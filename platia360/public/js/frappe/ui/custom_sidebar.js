// platia360/platia360/public/js/frappe/ui/custom_sidebar.js
console.log("%c[Custom Sidebar] Loaded with collapse, icons, dynamic workspaces", "color:#4CAF50;font-weight:bold;");

frappe.provide("frappe.ui");

frappe.ui.Sidebar = class CustomSidebar {
    constructor({ wrapper, css_class }) {
        console.log("%c[Custom Sidebar INSTANTIATED] Arguments:", "color:#FF9800;font-weight:bold;", args);
        console.log("Wrapper element:", args.wrapper[0]); // Logs the raw DOM element for easy inspection
        this.wrapper = wrapper;
        this.css_class = css_class;
        this.items = {};
        this.is_collapsed = false;
        this.make_dom();
        this.load_workspaces();
        this.bind_toggle();
    }

    make_dom() {
        this.wrapper.html(`
            <div class="${this.css_class} custom-sidebar dark-mode">
                
                <div class="sidebar-header">
                    <img src="/assets/your_app/img/logo.png" class="brand-logo">
                    <span class="brand-text">Your App</span>
                    <button class="collapse-btn">
                        <i class="fa fa-bars"></i>
                    </button>
                </div>

                <div class="sidebar-content"></div>
            </div>
        `);

        this.$sidebar = this.wrapper.find(".custom-sidebar");
        this.$content = this.$sidebar.find(".sidebar-content");
    }

    // Load Frappe Workspaces dynamically
    async load_workspaces() {
        const ws = await frappe.call("frappe.desk.desktop.get_workspace_sidebar_items");

        const pages = ws.message.pages || [];

        pages.forEach(page => {
            this.add_item({
                label: page.label,
                href: `/app/${page.public_page || page.name}`,
                icon: page.icon || "fa fa-circle",
                name: page.name,
            });
        });
    }

    add_item(item) {
        const active = window.location.pathname.includes(item.href) ? "active" : "";

        const html = `
            <div class="sidebar-item ${active}" data-name="${item.name}">
                <i class="${item.icon} sidebar-icon"></i>
                <span class="sidebar-label">${item.label}</span>
            </div>
        `;

        const $el = $(html);
        $el.click(() => frappe.set_route(item.href));

        this.$content.append($el);
        this.items[item.name] = $el;
    }

    bind_toggle() {
        this.wrapper.on("click", ".collapse-btn", () => {
            this.is_collapsed = !this.is_collapsed;

            if (this.is_collapsed) {
                this.$sidebar.addClass("collapsed");
            } else {
                this.$sidebar.removeClass("collapsed");
            }
        });
    }
};

