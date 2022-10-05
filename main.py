import dash_bootstrap_components as dbc
from pages import login_page, admin_page, payroll_page, user_info_page
from app import app


app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(children=login_page.login_page, label="Giriş", active_tab_style={"font-weight": "bold"}, id="login-tab",
                tab_id="login-tab"),
        dbc.Tab(children=user_info_page.user_info_page, label="Kullanici Bilgileri",
                active_tab_style={"font-weight": "bold"},
                id="user-info-tab", tab_id="user-info-tab", disabled=True),
        dbc.Tab(children=payroll_page.payroll_page, label="Maas Hesapla", active_tab_style={"font-weight": "bold"},
                id="payroll-tab", tab_id="payroll-tab", disabled=True),
        dbc.Tab(children=admin_page.admin_data_entry_page, label="Temel Veriler",
                active_tab_style={"font-weight": "bold"},
                tab_id="admin-data-entry-tab", id="admin-data-entry-tab", disabled=True),
        dbc.Tab(label="Çıkış", id="logout-tab", tab_id="logout-tab",
                tab_style={"marginLeft": "auto", "text-align": "right"}, disabled=True)],
        id="tabs", active_tab="login-tab")
])

if __name__ == '__main__':
    app.run_server(debug=True)
