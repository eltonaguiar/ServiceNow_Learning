/**
 * sn_probe.js — read YOUR ServiceNow instance and print a JSON fact sheet.
 *
 * Where to run it (either works):
 *   1. All > System Definition > Scripts - Background  (paste, tick "Run in sandbox" only if
 *      you know it has no side effects — it does not write anything), OR
 *   2. Create a Fix Script and run it once.
 *
 * Read-only by design: every query here is a get()/setLimit() read. It writes nothing,
 * changes nothing, and installs nothing. Safe on a PDI, safe on dev. Do not run on prod
 * without your platform owner's nod (it is harmless, but "harmless script on prod" is a
 * conversation).
 *
 * Then: copy the JSON between the BEGIN/END markers into a file and render it:
 *   python3 scripts/sn_sheet.py probe.json --out docs/generated/probe-sheet.md
 *
 * Why this exists: docs describe *a* release with *some* plugins. Your instance is the
 * authority on mandatory fields, related lists, what is installed and whether a Guided
 * Setup module exists at all.
 *
 * Agent: buffy (mimo-v2.6-flash) · 2026-11-04
 */

var PROBE = (function () {
    // ---- edit these if you want a different scope -------------------------
    var TABLES = [
        'incident', 'problem', 'change_request', 'task_sla',
        'cmdb_ci', 'cmdb_rel_ci',
        'alm_asset', 'alm_license', 'ast_contract',
        'sn_hr_core_case', 'sn_si_incident', 'sn_customerservice_case', 'wm_order',
        'sys_user', 'sys_user_group'
    ];
    // Foundation data: the layer every module assumes exists. Load order matters and has
    // nothing to do with process configuration, which is why it gets skipped.
    var FOUNDATION_TABLES = [
        'core_company', 'cmn_location', 'cmn_department', 'cmn_cost_center',
        'sys_user', 'sys_user_group', 'sys_user_group_type',
        'cmn_schedule'
    ];
    var MAX_ROWS = 60;        // per list, keeps the output readable
    var SAMPLE = 8;           // example names per section
    // -----------------------------------------------------------------------

    var out = {
        probe_version: '1.0.0',
        generated: gs.nowDateTime(),
        instance: gs.getProperty('instance_name') || 'unknown',
        release: gs.getProperty('glide.product.version') || 'unknown',
        release_name: gs.getProperty('com.glide.currency.release') || 'unknown',
        user: gs.getUserName(),
        tables: {},
        plugins: {},
        guided_setup: {},
        automation: {},
        apis: {},
        analytics: {},
        sam: {},
        foundation: {}
    };

    function safe(label, fn, fallback) {
        try {
            return fn();
        } catch (e) {
            out.errors = out.errors || [];
            out.errors.push(label + ': ' + e.message);
            return fallback;
        }
    }

    // ---- tables: mandatory fields + related lists -------------------------
    TABLES.forEach(function (table) {
        out.tables[table] = safe('table ' + table, function () {
            var info = { label: table, exists: false, mandatory: [], related_lists: [], row_count: null };

            var dbo = new GlideRecord('sys_db_object');
            if (!dbo.get('name', table)) {
                return info; // table not in this instance
            }
            info.exists = true;
            info.label = dbo.getValue('label') || table;
            info.super_class = dbo.getValue('super_class') || '';

            var dict = new GlideRecord('sys_dictionary');
            dict.addQuery('name', table);
            dict.addQuery('mandatory', true);
            dict.addQuery('element', '!=', '');
            dict.orderBy('element');
            dict.setLimit(MAX_ROWS);
            dict.query();
            while (dict.next()) {
                info.mandatory.push({
                    field: dict.getValue('element'),
                    type: dict.getValue('internal_type'),
                    label: dict.getValue('column_label')
                });
            }

            var rel = new GlideRecord('sys_ui_related_list');
            rel.addQuery('name', table);
            rel.setLimit(5);
            rel.query();
            while (rel.next()) {
                var entries = new GlideRecord('sys_ui_related_list_entry');
                entries.addQuery('sys_ui_related_list', rel.getUniqueValue());
                entries.orderBy('position');
                entries.setLimit(MAX_ROWS);
                entries.query();
                while (entries.next()) {
                    info.related_lists.push(entries.getValue('related_list'));
                }
            }

            var count = new GlideAggregate(table);
            count.addAggregate('COUNT');
            count.query();
            if (count.next()) {
                info.row_count = parseInt(count.getAggregate('COUNT'), 10) || 0;
            }
            return info;
        }, { label: table, exists: false, mandatory: [], related_lists: [], row_count: null });
    });

    // ---- foundation data: counts, missing, empty --------------------------
    out.foundation = safe('foundation', function () {
        var counts = {};
        var missing = [];
        FOUNDATION_TABLES.forEach(function (t) {
            var dbo = new GlideRecord('sys_db_object');
            if (!dbo.get('name', t)) { missing.push(t); return; }
            var agg = new GlideAggregate(t);
            agg.addAggregate('COUNT');
            agg.query();
            counts[t] = agg.next() ? (parseInt(agg.getAggregate('COUNT'), 10) || 0) : 0;
        });
        var empty = [];
        for (var k in counts) { if (counts[k] === 0) { empty.push(k); } }

        // Users with no org dimensions are the symptom that shows up in every bad report.
        function countWhere(table, field) {
            var gr = new GlideAggregate(table);
            gr.addQuery(field, 'EMPTY');
            gr.addAggregate('COUNT');
            gr.query();
            return gr.next() ? (parseInt(gr.getAggregate('COUNT'), 10) || 0) : 0;
        }
        var hygiene = safe('foundation hygiene', function () {
            return {
                users_without_department: countWhere('sys_user', 'department'),
                users_without_manager: countWhere('sys_user', 'manager'),
                users_without_location: countWhere('sys_user', 'location'),
                groups_without_manager: countWhere('sys_user_group', 'manager'),
                locations_without_time_zone: countWhere('cmn_location', 'time_zone')
            };
        }, {});

        // Which schedule-ish tables this release actually has (names vary).
        var schedule_tables = [];
        var sched = new GlideRecord('sys_db_object');
        sched.addQuery('name', 'STARTSWITH', 'cmn_');
        sched.orderBy('name');
        sched.setLimit(30);
        sched.query();
        while (sched.next()) { schedule_tables.push(sched.getValue('name')); }

        return { counts: counts, missing: missing, empty: empty, hygiene: hygiene,
                 cmn_tables: schedule_tables };
    }, {});

    // ---- plugins / installed apps ----------------------------------------
    out.plugins = safe('plugins', function () {
        var found = [];
        var gr = new GlideRecord('v_plugin');
        gr.addQuery('active', true);
        gr.orderBy('name');
        gr.setLimit(MAX_ROWS);
        gr.query();
        while (gr.next()) {
            found.push({
                id: gr.getValue('id'),
                name: gr.getValue('name'),
                version: gr.getValue('version')
            });
        }
        return { total_listed: found.length, items: found };
    }, {});

    // ---- guided setup modules --------------------------------------------
    out.guided_setup = safe('guided_setup', function () {
        var mods = [];
        var gr = new GlideRecord('sys_app_module');
        gr.addQuery('title', 'CONTAINS', 'Guided Setup');
        gr.addQuery('active', true);
        gr.orderBy('title');
        gr.setLimit(MAX_ROWS);
        gr.query();
        while (gr.next()) {
            mods.push({ title: gr.getValue('title'), target: gr.getValue('name') });
        }
        return { count: mods.length, modules: mods };
    }, {});

    // ---- automation: flows ------------------------------------------------
    out.automation = safe('automation', function () {
        var agg = new GlideAggregate('sys_hub_flow');
        agg.addAggregate('COUNT');
        agg.query();
        var total = 0;
        if (agg.next()) {
            total = parseInt(agg.getAggregate('COUNT'), 10) || 0;
        }
        var active = new GlideAggregate('sys_hub_flow');
        active.addQuery('active', true);
        active.addAggregate('COUNT');
        active.query();
        var activeCount = 0;
        if (active.next()) {
            activeCount = parseInt(active.getAggregate('COUNT'), 10) || 0;
        }
        var samples = [];
        var gr = new GlideRecord('sys_hub_flow');
        gr.addQuery('active', true);
        gr.orderByDesc('sys_updated_on');
        gr.setLimit(SAMPLE);
        gr.query();
        while (gr.next()) {
            samples.push(gr.getValue('name'));
        }
        return { flows_total: total, flows_active: activeCount, recent_active: samples };
    }, {});

    // ---- apis -------------------------------------------------------------
    out.apis = safe('apis', function () {
        function countOf(table, extra) {
            var gr = new GlideAggregate(table);
            if (extra) { extra(gr); }
            gr.addAggregate('COUNT');
            gr.query();
            return gr.next() ? (parseInt(gr.getAggregate('COUNT'), 10) || 0) : 0;
        }
        return {
            scripted_rest_apis: countOf('sys_ws_definition', null),
            rest_messages: countOf('sys_rest_message', null)
        };
    }, {});

    // ---- analytics --------------------------------------------------------
    out.analytics = safe('analytics', function () {
        function countOf(table) {
            var gr = new GlideAggregate(table);
            gr.addAggregate('COUNT');
            gr.query();
            return gr.next() ? (parseInt(gr.getAggregate('COUNT'), 10) || 0) : 0;
        }
        return {
            indicators: safe('pa_indicators', function () { return countOf('pa_indicators'); }, null),
            reports: safe('sys_report', function () { return countOf('sys_report'); }, null),
            dashboards: safe('pa_dashboards', function () { return countOf('pa_dashboards'); }, null)
        };
    }, {});

    // ---- SAM presence -----------------------------------------------------
    out.sam = safe('sam', function () {
        var tables = [];
        var gr = new GlideRecord('sys_db_object');
        var q = gr.addQuery('name', 'STARTSWITH', 'samp_');
        q.addOrCondition('name', 'STARTSWITH', 'cmdb_sam_');
        gr.orderBy('name');
        gr.setLimit(40);
        gr.query();
        while (gr.next()) {
            tables.push(gr.getValue('name'));
        }
        return {
            sam_tables_found: tables.length,
            tables: tables,
            note: 'SAM Foundation and SAM Pro differ. If this list is empty, no SAM schema is installed.'
        };
    }, {});

    return out;
})();

gs.info('=== SNPROBE BEGIN ===');
gs.info(JSON.stringify(PROBE));
gs.info('=== SNPROBE END ===');

// Also return it so a Fix Script / background script shows it as the response:
JSON.stringify(PROBE, null, 2);
