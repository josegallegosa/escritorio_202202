odoo.define('savar_oms_catalog.web_editor', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var dialog = require('web.Dialog');

    var _t = core._t;

    publicWidget.Widget.include({
        init: function (parent, action) 
        {
            var self = this;

            $('a.add_form_line').unbind('click');            
            $( document ).ready(function() {
                $('table.table_order_lines input.line_product').first().click();                
            });            
            
            $('a.add_form_line').off('click');
            $('a.add_form_line').click(function (event) 
            {
                event.preventDefault();
                self.add_form_line();
                self._start_product_line_002($('table.table_order_lines input.line_product').last());
            });

            $('div.action_remove_line').unbind('click');
            $(document).off('click');
            $(document).on('click','div.action_remove_line', function (event) 
            {             
                event.preventDefault();                
                $(this).unbind('click');
                self.remove_form_line($(this));
            }); 

            $('#order_partner').unbind('change');
            $("#order_partner").on('change', function(){
                self._start_partner_invoice_002();
                self._start_partner_delivery_002();
            });

            $('.line_product').unbind('click');
            $(document).off('click');
            $(document).on('click', "input.line_product", function(event){                
                event.preventDefault();                
                self._start_product_line_002($(this));
            });

            $('.line_product').unbind('change');
            $(document).off('change');
            $(document).on('change',".line_product", function(event){
                event.preventDefault();
                self._start_product_line_values_002($(this));

                var product_id = $(this).closest('tr').find('input.line_product').val();
                var selector = $(this).closest('tr').find('input.line_subservice');
                
                var params = {
                    '_product_id':product_id,
                    '_selector':selector,
                    '_route':'/selections/products/get_product_services',
                    '_fields':['id', 'name'],
                    '_domain':[['parent_id','!=',null]],
                    '_multiple':false,
                 }     

                self._start_product_line_subservice_002(params);

            }); 

            $('.line_price').unbind('change'); 
            $(document).on('change',".line_price",function(event){
                event.preventDefault();
                self._update_product_line_values_002($(this));
            });

            $('.line_quantity').unbind('change'); 
            $(document).on('change',".line_quantity",function(event){
                event.preventDefault();
                self._update_product_line_values_002($(this));
            });

            $('.go_back_order').unbind('click'); 
            $(document).on('click',".go_back_order",function(event){
                event.preventDefault();
                window.location.href = location.protocol + '//' + location.host + '/my/home'
            });
            
            $(document).on('click', "a.save_order", function(event){                
                event.preventDefault();                
                self.save_merchant_order($(this));
            });

            self._start_partner_002();

            this._super(parent, action);
        },        
        disable_merchant_new_order_form: function()
        {
            $("#order_partner").attr('readonly','1');
            $("#order_partner_invoice_address").attr('readonly','1');
            $("#order_partner_delivery_address").attr('readonly','1');

            $(".line_product").attr('readonly','1');
            $(".line_description").attr('readonly','1');
            $(".line_quantity").attr('readonly','1');
            $(".line_price").attr('readonly','1');
            $(".line_tax").attr('readonly','1');
            $(".line_total").attr('readonly','1');
            $(".action_remove_line").attr('disable','1');
            $(".add_form_line").attr('disable','1');
            $(".save_order").fadeIn();            
        },
        enable_merchant_new_order_form: function()
        {
            $("#order_partner").removeAttr('readonly');
            $("#order_partner_invoice_address").removeAttr('readonly');
            $("#order_partner_delivery_address").removeAttr('readonly');

            $(".line_product").removeAttr('readonly');
            $(".line_description").removeAttr('readonly');
            $(".line_quantity").removeAttr('readonly');
            $(".line_price").removeAttr('readonly');
            $(".line_tax").removeAttr('readonly');
            $(".line_total").removeAttr('readonly');
            $(".action_remove_line").removeAttr('readonly');
            $(".add_form_line").attr('disable','1');      
            $(".save_order").fadeIn();           
        },
        save_merchant_order: function()
        {
            var self = this;
            var partner_id = $('#order_partner').val();
            var partner_invoice_id = $('#order_partner_invoice_address').val();
            var partner_delivery_id = $('#order_partner_delivery_address').val();
            var lines = [];

            $("table.table_order_lines tr.order_line").each(function()
            {
                var selector_line = $(this);                
                var product_id = selector_line.find("input.line_product").val();
                var product_description = selector_line.find("input.line_description").val();
                var product_quantity = selector_line.find("input.line_quantity").val();
                var product_price = selector_line.find("input.line_price").val();
                var product_tax = selector_line.find("input.line_tax").val();
                var product_subservice = selector_line.find("input.line_subservice").val();
                
                var line = {
                                'product_id': product_id,
                                'product_description': product_description,
                                'product_quantity': product_quantity,
                                'product_price': product_price,
                                'product_taxes': product_tax,
                                'product_subservice':product_subservice
                           };
                lines.push(line);
            });

            var sequence = $("input[name='order_name']").val();

            rpc.query({
                route: '/orders/create',
                params: {
                    sequence:sequence,
                    partner_id:partner_id,
                    partner_invoice_id:partner_invoice_id,
                    partner_delivery_id:partner_delivery_id,
                    lines: lines,
                }
            }).then(function (order) {                
                if(order)
                {
                    order = order[0];
                    if( order.id )
                    {
                        dialog.alert(null, "El pedido " + String(order.name) + String("fue creado exitosamente."), {});
                        self.disable_merchant_new_order_form();
                    }
                }
            }); 

        },
       preselection_line_taxes_003: function(taxes, selector){
            var self = this;

            if(taxes)
            {
                rpc.query({
                    route: '/selections/taxes/get_taxes_assigned',
                    params: {
                        fields: ['id','name'],
                        domain: [['id','in',taxes]],
                    }
                }).then(function (taxes_assigned) {
                    if(taxes_assigned.taxes)
                    {
                        var _taxes = taxes_assigned.taxes;
                        var _input_value = String();
                        _taxes.forEach(function(tax){
                            
                            var li = $("<li class='select2-search-choice'/>");
                            var li_text = $("<div>"+String(tax.text)+"<div/>");
                            var li_a_delete = $("<a href='#' class='select2-search-choice-close custom_tax_delete' tabindex='-1' data-id='"+String(tax.id)+"' />");
                            
                            li_a_delete.on('click', function () 
                            {
                                self.delete_preselection_tag_003($(this));
                            });
                            var option = li.append(li_text).append(li_a_delete);                    
                            selector.closest('tr').find("ul.select2-choices").prepend(option);

                            _input_value = String(_input_value) + String(parseInt(tax.id)) + String(",");
                        });

                        console.log('_input_value');

                        if( String(_input_value).length>0 )
                        {
                            console.log(_input_value);
                            _input_value = String(_input_value).slice(0, -1);
                            console.log(_input_value);
                            selector.closest('tr').find('input.line_tax').val(_input_value);
                        }
                    }                    
                });               
            }          
        },
        delete_preselection_tag_003: function(element){

            var tags = element.closest('tr').find("input.line_tax").val();
            var _id = element.attr("data-id");
            tags = tags.replace(_id, 0);
            tags = tags.replace(',,', ',');
            try
            {
                tags = String(tags).split(',');
                var _tags = [];
                if(tags)
                {
                   try
                   {
                    tags.forEach(function(_tag){
                        try
                        {
                            if(parseInt(_tag)>0)
                            {
                                _tags.push(parseInt(_tag));
                            }
                        }
                        catch(ex)
                        {}
                    }); 
                   }
                   catch(ex)
                   {}
                }
                tags = _tags;
                selector.find(".line_tax").val(_tags);
            }
            catch(ex)
            {}

            element.closest("li").remove();
        },
        _update_product_line_values_002: function(selector)
        {
            var self = this;
            var line_price = selector.closest('tr').find('.line_price').val();
            var line_quantity = selector.closest('tr').find('.line_quantity').val();
            var linte_total = self.get_line_total({'qty':line_quantity, 'price':line_price});
            selector.closest('tr').find('.line_total').val(linte_total);
            self.calculate_lines_total();
        },
        _start_product_line_values_002: function (selector) 
        {
            var self = this;
            var product_id = selector.val();
            rpc.query({
                route: '/selections/products/get_products',
                params: {
                    fields: ['id','name','virtual_available', 'list_price', 'taxes_id'],
                    domain: [['id','=',product_id]],
                }
            }).then(function (data) {
                if(data.read_results)
                {
                    if( data.read_results.length>0 )
                    {
                        var product = data.read_results[0];
                        self._start_line_taxes_selector_002(selector.closest('tr').find('.line_tax'));
                        selector.closest('tr').find('.line_description').val(product.name);
                        selector.closest('tr').find('.line_price').val(product.list_price);
                        selector.closest('tr').find('.line_quantity').val(1);
                        var line_total = self.get_line_total({'qty':1, 'price':product.list_price})
                        selector.closest('tr').find('.line_total').val(line_total);
                        selector.closest('tr').find('.line_description').removeAttr('readonly');
                        self.preselection_line_taxes_003(product.taxes_id, selector);
                        self.calculate_lines_total();
                    }                    
                }
            });
        },
        format_money: function(_number)
        {
            return new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(_number)            
        },
        calculate_lines_total: function()
        {
            var self = this;
            var total = parseFloat(0.0);
            $('table.table_order_lines input.line_total').each(function(index, subtotal)
            {
                var subtotal = $(this).val();
                total += parseFloat(subtotal);
            });
            $("label.table_order_total").text(self.format_money(total));
        },
        get_line_total: function(params)
        {
            var total = parseFloat(params['qty']) * parseFloat(params['price']);
            return total;
        },
        add_form_line: function () 
        {
            var default_line = $('table.default_order_line_table').find('tbody');
            var _html = default_line.html();
            var remove_action = default_line.find('div.action_remove_line');
            $('table.table_order_lines').append(_html);
        },
        remove_form_line: function (element) 
        {
            element.closest('tr').remove();
        },
        _start_partner_002: function () {            
            var self = this;
            var order_partner_element = $('#order_partner');
            order_partner_element.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: false,
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        rpc.query({
                            route: '/selections/partner/get_partners',
                            params: {
                                fields: ['id','name'],
                                domain: [], // domain: [['type_tax_use','=','sale']],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
        _start_partner_invoice_002: function () {            
            var self = this;
            var parent_id = $('#order_partner').val();
            var order_partner_invoice_address_element = $('#order_partner_invoice_address');
            order_partner_invoice_address_element.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: false,
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        rpc.query({
                            route: '/selections/partner/get_invoice_partner_childs',
                            params: {
                                fields: ['id','name'],
                                domain: ["|", ['id','=',parseInt(parent_id)], ['parent_id','in',[parseInt(parent_id)] ]],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
        _start_partner_delivery_002: function () {            
            var self = this;
            var parent_id = $('#order_partner').val();
            var order_partner_delivery_address_element = $('#order_partner_delivery_address');
            order_partner_delivery_address_element.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: false,
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        rpc.query({
                            route: '/selections/partner/get_invoice_partner_childs',
                            params: {
                                fields: ['id','name'],
                                domain: ["|", ['id','=',parseInt(parent_id)], ['parent_id','in',[parseInt(parent_id)] ]],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
        _start_product_line_002: function (selector) {            
            var self = this;
            selector.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: false,
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        rpc.query({
                            route: '/selections/products/get_products',
                            params: {
                                fields: ['id','name'],
                                domain: [],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
        _start_product_line_subservice_002: function (_arguments) {            
            var self = this;
            console.log(_arguments);
            _arguments['_selector'].select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: _arguments['_multiple'],
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    if (!this.selection_data) {
                        rpc.query({
                            route: _arguments['_route'],
                            params: {
                                product_id: _arguments['_product_id'],
                                fields: _arguments['_fields'],
                                domain: _arguments['_domain'],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
        _start_line_taxes_selector_002: function (selector) {            
            var self = this;
            selector.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: true,
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        rpc.query({
                            route: '/selections/taxes/search_read',
                            params: {
                                fields: ['id','name'],
                                domain: [['type_tax_use','=','sale']],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
        
    });
});