odoo.define('savar_oms_catalog.product_taxes', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    publicWidget.Widget.include({
        init: function (parent, action) {
            var self = this;
            this._super(parent, action);
        },
    });
});