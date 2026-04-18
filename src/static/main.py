from pyscript import web, when, display

test_tasks = {"UUID": {"Description": "Test Task",
                       "Project": "Test Project",
                       "Tags": "Test Tag",
                       "Due Date": "2023-01-01"},
              "UUID2": {"Description": "Test Task 2",
                        "Project": "Test Project 2",
                        "Tags": "Test Tag 2",
                        "Due Date": "2023-01-02"}}


def create_tabs():
    tab_div = web.page.find("#due_dates")
    tab_div[0].append(web.ul(web.li(web.a("Overdue", id="overdueTab"), classes="date-tabs"),
                             web.li(web.a("Due Today",id="todayTab"), classes="date-tabs"),
                             web.li(web.a("Due this Month",id="monthTab"), classes="date-tabs"),
                             web.li(web.a("All Incomplete Tasks",id="incompleteTab"), classes="date-tabs is-active"),
                             web.li(web.a("Completed Tasks", id="completedTab"), classes="date-tabs")))



def create_task_table(tasks):
    table_body = web.page.find("#task_table_body")
    for uuid, task in tasks.items():
        table_body[0].append(web.tr(web.td(task["Description"]), web.td(task["Project"]),
                                    web.td(task["Tags"]), web.td(task["Due Date"]),
                                    web.td(web.button("Modify", classes="button is-blue")),
                                    web.td(web.button("Completed", classes="button is-blue")), id=uuid))




# Add to the page.
create_tabs()
create_task_table(test_tasks)

@when("click", ".date-tabs")
def change_tab_highlight(event):
    _id = event.target.id
    tabs = web.page.find(".date-tabs")
    for tab in tabs:
        tab.classes.remove("is-active")
    selected_tab = web.page.find(f"#{_id}")
    selected_tab[0].parent.classes.add("is-active")
