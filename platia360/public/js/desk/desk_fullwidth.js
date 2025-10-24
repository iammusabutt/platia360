// desk_fullwidth.js
(function() {
    // safe guard
    if (!window.jQuery) return console.warn("jQuery not found - desk_fullwidth aborted");

    frappe.after_ajax(function() {
        const $doc = $(document);

        function patchWrapper($wrapper) {
            if (!$wrapper || !$wrapper.length) return;

            // body container (redundant safety)
            $wrapper.find(".container.page-body").addBack(".container.page-body")
                .removeClass("container")
                .addClass("container-fluid");

            // page head container (title/header)
            $wrapper.find(".page-head > .container").addBack(".page-head > .container")
                .removeClass("container")
                .addClass("container-fluid");
        }

        // --- 🧩 Patch global Desk navbar (outside wrapper)
        function patchNavbar() {
            const $navbar = $(".navbar > .container");
            if ($navbar.length) {
                $navbar.removeClass("container").addClass("container-fluid nav-holder");
            }
        }

        // 1) Extend known view classes so change happens during make()
        const view_names = ["ListView", "FormView", "KanbanView", "ReportView", "GanttView", "Workspace"];
        view_names.forEach(name => {
            try {
                const Orig = frappe.views[name];
                if (!Orig) return;
                frappe.views[name] = class extends Orig {
                    make() {
                        // call original
                        if (super.make) super.make();
                        try {
                            // many views keep $page.wrapper, some may use this.wrapper or this.$wrapper
                            const wrapper = (this.$page && this.$page.wrapper) || this.$wrapper || this.wrapper || $(document.body);
                            patchWrapper($(wrapper));
                        } catch (e) {
                            console.warn("desk_fullwidth patch error for", name, e);
                        }
                    }
                };
            } catch (e) {
                console.warn("desk_fullwidth unable to extend", name, e);
            }
        });

        // 2) MutationObserver fallback for dynamically inserted nodes
        const observer = new MutationObserver(mutations => {
            for (const m of mutations) {
                if (!m.addedNodes) continue;
                m.addedNodes.forEach(node => {
                    if (!(node instanceof HTMLElement)) return;
                    const $node = $(node);
                    if (
                        $node.is(".container.page-body") ||
                        $node.find(".container.page-body").length ||
                        $node.is(".page-head > .container") ||
                        $node.find(".page-head > .container").length
                    ) {
                        try {
                            patchWrapper($node);
                        } catch (e) {
                            console.warn("desk_fullwidth observer patch error", e);
                        }
                    }
                });
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });

        // 3) Run once for existing content
        patchWrapper($doc);

        // 4) Patch the top Desk navbar once now
        patchNavbar();

        // 5) Reapply if navbar is re-rendered dynamically
        const navObserver = new MutationObserver(patchNavbar);
        navObserver.observe(document.body, { childList: true, subtree: true });
    });
})();
