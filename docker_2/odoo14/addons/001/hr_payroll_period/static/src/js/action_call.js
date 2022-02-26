

odoo.define('invoice.action_button', function (require) {
"use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var QWeb = core.qweb;
    var PeriodsListController = ListController.extend({
        renderButtons: function () {
            this._super.apply(this, arguments);
            this.$buttons.append($(QWeb.render("PeriodsListView.buttons", this)));
            var self = this;
            this.$buttons.on('click', '.generate_period', function () {
            	/*
                if (self.getSelectedIds().length == 0) {
                    return;
                }*/
                return self._rpc({
                    model: 'hr.payroll.period',
                    method: 'generate_wizard_period',
                    args: [self.getSelectedIds()],
                }).then(function (results) {
                    self.do_action(results);
                });
            });
        }
    });

    var PeriodsListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: PeriodsListController,
        }),
    });

    viewRegistry.add('payroll_period_tree', PeriodsListView);
});