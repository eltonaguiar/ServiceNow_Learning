# 03 — Breadcrumbs: where the important things actually live

> **Agent:** buffy (mimo-v2.6-flash) · **Branch:** buffy-mimo-v2.6-flash-2026-11-04 · **Updated:** 2026-11-04

Menus move between releases and change with which plugins are installed. So: every path
below is a **starting point**, and every module lists the *table* it belongs to — because
typing a table name into the filter navigator always works, even when the menu label moved.

**The universal escape hatch:** if you cannot find a module, open
`All > System Definition > Application Menus` (`sys_app_module`) and filter `Title` — that
is the record behind every menu item on the platform.

---

## The 12 bookmarks that cover 80% of the work

| # | Path | Table / what it is |
|---|---|---|
| 1 | `All > System Definition > Tables & Columns` | `sys_db_object`, `sys_dictionary` — the map of everything |
| 2 | `All > System Definition > Application Menus` | `sys_app_module` — why a menu item exists |
| 3 | `All > System Applications > All Available Applications` | what is installed vs installable |
| 4 | `All > System Logs > All` | `syslog` — real errors live here |
| 5 | `All > System Logs > Outbound HTTP Requests` | `sys_outbound_http_log` — every integration bug starts here |
| 6 | `All > Process Automation > Flow Designer` | `sys_hub_flow` — all automation |
| 7 | `All > Process Automation > Process Automation Designer` | playbooks |
| 8 | `All > System Web Services > Scripted REST APIs` | `sys_ws_definition` — APIs you publish |
| 9 | `All > System Web Services > Outbound > REST Message` | `sys_rest_message` — APIs you call |
| 10 | `All > User Administration > Users` → impersonate | `sys_user` — see it as the user |
| 11 | `All > System Update Sets > Local Update Sets` | `sys_update_set` — how changes travel |
| 12 | `All > System Definition > Scripts - Background` | the probe / one-off scripts |

---

## By module

### Platform
| You want | Path | Table |
|---|---|---|
| Understand any field | Tables & Columns → search table → Columns | `sys_dictionary` |
| See all modules | Application Menus | `sys_app_module` |
| Check a property | `All > System Properties > All Properties` | `sys_properties` |
| Roles and what they grant | `All > User Administration > Roles` | `sys_user_role` |
| Find a scheduled job | `All > System Scheduler > Scheduled Jobs` | `sys_trigger` |

### Incident / Problem / Change
| You want | Path | Table |
|---|---|---|
| Create an incident | `All > Incident > Create New` | `incident` |
| My work | `All > Incident > Assigned to me` | `incident` |
| SLA definitions | `All > Service Level Management > SLA Definitions` | `contract_sla` |
| SLA on one record | Open incident → **Task SLA** related list | `task_sla` |
| Change types/approvals | `All > Change > Create New` then read **Type** | `change_request` |
| Standard change templates | `All > Change > Standard Change Catalog` | `std_change_producer_version` |
| CAB | `All > Change > CAB Workbench` | `cab_meeting` (verify) |
| Problem / known error | `All > Problem > Open` / `> Known Errors` | `problem`, `known_error` |

### CMDB / ITOM
| You want | Path | Table |
|---|---|---|
| CI list | `All > Configuration Management Database > CMDB Workspace` | `cmdb_ci` |
| Class model | `All > Configuration Management Database > CI Class Manager` | `cmdb_ci` hierarchy |
| **Identification rules** | `All > Configuration Management > CI Identifiers` | duplicate prevention |
| Health | `All > Configuration Management > Health > CMDB Health Dashboard` | health jobs |
| Relationships | Open a CI → **Relationships** related list | `cmdb_rel_ci` |
| Discovery | `All > Discovery > Home` | discovery schedules |

### SAM / ITAM
| You want | Path | Table |
|---|---|---|
| All assets | `All > Asset > Portfolios > All Assets` | `alm_asset` |
| Hardware assets | `All > Asset > Assets > Hardware` | `alm_hardware` |
| Licences | `All > Asset > Assets > Licenses` / SAM licence operations | `alm_license` (verify per edition) |
| Contracts | `All > Asset > Contracts > All` | `ast_contract` |
| Software products / normalisation | SAM admin menus | `samp_*` / `cmdb_sam_*` — **verify with probe** |
| Compliance position | SAM dashboard / licence position | reconciliation output |

### HRSD
| You want | Path | Table |
|---|---|---|
| Cases | `All > HR > Cases > All` | `sn_hr_core_case` |
| What employees can request | `All > HR > Administration > HR Services` | `sn_hr_core_service` (verify) |
| Lifecycle events | `All > HR > Lifecycle Events` | `sn_hr_le_*` |
| Portal | Employee Center | — |

### SecOps
| You want | Path | Table |
|---|---|---|
| Security incidents | `All > Security Operations > Security Incidents` | `sn_si_incident` |
| Alerts | `All > Security Operations > All Alerts` | `sn_si_alert` |
| Ingestion profiles | `All > Security Operations > Administration > Alert Ingestion` | integration profiles |
| Observables / intel | `All > Security Operations > Threat Intelligence` | `sn_si_observable` |

### CSM
| You want | Path | Table |
|---|---|---|
| Cases | `All > Customer Service > Cases > All` | `sn_customerservice_case` |
| Accounts | `All > Customer Service > Accounts` | `customer_account` |
| Entitlements | `All > Customer Service > Administration > Entitlements` | `sn_customerservice_entitlement` |
| Portal | Customer Service Portal | — |

### FSM
| You want | Path | Table |
|---|---|---|
| Work orders | `All > Field Service Management > Work Orders` | `wm_order` |
| Dispatch | `All > Field Service Management > Dispatch > Dispatch Board` | — |
| Territories | `All > Field Service Management > Administration > Territories` | `wm_territory` |
| Constraints | `All > Field Service Management > Administration > Scheduling > Constraints` | — |

### Integration
| You want | Path | Table |
|---|---|---|
| Call an API | `All > System Web Services > Outbound > REST Message` | `sys_rest_message` |
| Publish an API | `All > System Web Services > Scripted REST APIs` | `sys_ws_definition` |
| Remote table | `All > System Web Services > Remote Tables` | `sys_remote_table` (verify) |
| OAuth credentials | `All > System OAuth > Application Registry` | `oauth_entity` |
| Why a call failed | `All > System Logs > Outbound HTTP Requests` | `sys_outbound_http_log` |
| Import sets | `All > System Import Sets > Load Data` | `sys_import_set` |

### Analytics
| You want | Path | Table |
|---|---|---|
| Indicators | `All > Platform Analytics > Indicators` | `pa_indicators` |
| Slices of a metric | `All > Platform Analytics > Breakdowns` | `pa_breakdowns` |
| Dashboards | `All > Platform Analytics > Dashboards` | `pa_dashboards` |
| Classic reports | `All > Reports > View / Create New` | `sys_report` |
| What keeps scores fresh | `All > Platform Analytics > Data Collector` | `pa_collector` (verify) |

---

## URL tricks that save minutes

- Jump straight to a list: `https://<instance>/nav_to.do?uri=incident_list.do`
- Jump to a module by name: `...?uri=navpage.do` then use the navigator
- Filter a list with a query you already know: append `?sysparm_query=active=true^priority=1`
- Open a record by id: `...?uri=incident.do?sys_id=<sys_id>`
- See a table's schema fast: `...?uri=sys_db_object.do?sys_id=...` from the table record

---

## Official sources

- Product documentation (application menus, navigation, module reference) — <https://www.servicenow.com/docs/> (read 2026-11-04)
- Now Create Success Packs (per-app module maps) — <https://learning.servicenow.com/lxp> search "Now Create" (read 2026-11-04)
- Community (when a module moved in a release) — <https://community.servicenow.com/> (read 2026-11-04)
