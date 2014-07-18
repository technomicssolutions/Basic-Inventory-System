/************* Common JS Methods ****************************/
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function get_items($scope, $http, from) {
    if (from == 'sales') {
        $scope.project_id = $scope.sales.project_id;
    } else if (from == 'dn') {
        $scope.project_id = $scope.delivery_note.project_id;
    } else {
        $scope.project_id = $scope.purchase.project_id;
    }
    
    if ($scope.project_id == 'select' || $scope.project_id == 'other' || $scope.project_id == undefined) {
        $scope.project_id = '';
    } else {
        if (from == 'sales') {
            $scope.project_id = $scope.sales.project_id;
        } else if (from == 'dn') {
            $scope.project_id = $scope.delivery_note.project_id;
        } else {
            $scope.project_id = $scope.purchase.project_id;
        }
    }
    $http.get('/project/items/?project_id='+$scope.project_id).success(function(data)
    {   
        if (from == 'sales' || from == 'dn') {
            $scope.items = data.project_items;
        } else {
            $scope.items = data.items;
        }
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function get_project_items($scope, $http, parameter, param, from) {
    // $scope.items = [];
    var url = '';
    if (from == 'dn') {
        var url = '/project/project_items/?project_id='+$scope.delivery_note.project_id+'&'+parameter+'='+param
    } else {
        var url = '/project/project_items/?project_id='+$scope.sales.project_id+'&'+parameter+'='+param
    }

    $http.get(url).success(function(data)
    {
        if (data.project_items.length == 0) {
            $scope.item_select_error = 'Item not found';
            $scope.item_selected = true;
        } else {
            $scope.item_select_error = '';
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.project_items;
        }
        
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function get_inventory_items($scope, $http, parameter, param){
    $http.get('/project/items/?inventory_item=true&'+parameter+'='+param).success(function(data)
    {
        if (data.inventory_items.length == 0) {
            $scope.item_select_error = 'Item not found';
        } else {
            $scope.item_select_error = '';
            $scope.selecting_item = true;
            $scope.item_selected = false;
            $scope.items = data.inventory_items;
        }
        
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function item_validation($scope, $http) {
    if ($scope.item.name == '' || $scope.item.name == undefined) {
        $scope.validation_error = 'Please ente the Name';
        return false;
    } else if ($scope.item.code == '' || $scope.item.code == undefined) {
        $scope.validation_error = 'Please enter the Code';
        return false;
    } else if ($scope.item.type == '' || $scope.item.type == undefined) {
        $scope.validation_error = 'Please choose the Type';
        return false;
    }
    return true;
}

function add_item($scope, $http, from) {
    $scope.is_valid = item_validation($scope, $http);
    if ($scope.is_valid) {
        params = { 
            'item_details': angular.toJson($scope.item),
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/project/add_item/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            if (from != 'add_item') {
                $scope.item = {
                    'id': '',
                    'name': '',
                    'code': '',
                    'current_stock': '',
                    'type': '',
                }
            }
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
            } else {
                if (from == 'add_item') {
                    document.location.href = '/project/items/';
                } else {
                    get_items($scope, $http, 'purchase');
                    $scope.item = data.item;
                    var selected_item = {
                        'item_code': data.item[0].code,
                        'item_name': data.item[0].name,
                        'current_stock': data.item[0].current_stock,
                        'selling_price': 0,
                        'qty_purchased': 0,
                        'cost_price': 0,
                        'net_amount': 0,
                        'unit_price': 0,
                        'type': data.item[0].type,
                    }
                    $scope.purchase.purchase_items.push(selected_item);
                    $scope.item_select_error = '';
                    $scope.close_popup();
                }
                
            }
        }).error(function(data, success){
            
        });
    }
}

function get_projects($scope, $http) {
    $http.get('/project/projects/').success(function(data)
    {   
        $scope.projects = data.projects;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function get_suppliers($scope, $http) {
    $http.get('/supplier/list/').success(function(data)
    {
        $scope.suppliers = data.suppliers;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function validate_add_supplier($scope) {
    $scope.validation_error = '';

    if($scope.name == '' || $scope.name == undefined) {
        $scope.validation_error = "Please Enter the supplier Name" ;
        return false;
    } else if($scope.contact_person == '' || $scope.contact_person == undefined) {
        $scope.validation_error = "Please enter the Contact Person";
        return false;
    } else if($scope.mobile == ''|| $scope.mobile == undefined){
        $scope.validation_error = "Please enter the Mobile Number";
        return false;
    } else if(!(Number($scope.mobile)) || $scope.mobile.length > 15) {            
        $scope.validation_error = "Please enter a Valid Mobile Number";
        return false;
    } else if(($scope.email == '' || $scope.email == undefined)){
        $scope.validation_error = "Please enter an Email Id";
        return false;         
    } else if (!(validateEmail($scope.email))) {
        $scope.validation_error = "Please enter a Valid Email Id";
        return false;
    }
    return true;
}

function add_new_supplier($scope, $http) {
    if(validate_add_supplier($scope)) {
        params = { 
            'name':$scope.name,
            'contact_person': $scope.contact_person,
            'house': $scope.house,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.phone,
            'email': $scope.email,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/register/supplier/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
            } else {
                $scope.popup.hide_popup();                             
                get_suppliers($scope, $http);
                $scope.purchase.supplier_name = $scope.supplier_name;
                $scope.purchase.supplier_name = data.supplier_name;
                $scope.supplier_name = '';
                $scope.contact_person = '';
                $scope.house_name = '';
                $scope.street = '';
                $scope.city = '';
                $scope.district = '';
                $scope.pin = '';
                $scope.mobile = '';
                $scope.land_line = '';
                $scope.email_id = '';
            }
        }).error(function(data, success){
            console.log(data || "Request failed");
        });
    }
}

function get_companies($scope, $http) {
    $http.get('/company_list/').success(function(data)
    {
        $scope.companies = data.company_names;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function add_new_company($scope, $http) {
    params = { 
        'new_company':$scope.company_name,
        "csrfmiddlewaretoken" : $scope.csrf_token
    }
    $http({
        method : 'post',
        url : "/add_company/",
        data : $.param(params),
        headers : {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
    }).success(function(data, status) {
        
        if (data.result == 'error'){
            $scope.error_flag=true;
            $scope.message = data.message;
        } else {
            $scope.popup.hide_popup();
            get_companies($scope, $http);
            $scope.purchase.transport = $scope.company_name;
            $scope.company_name = '';
            $scope.message = '';
        }
    }).error(function(data, success){
        
    });
}

function get_customers($scope, $http) {
    $http.get('/customer/list/').success(function(data)
    {   
        
        $scope.customers = data.customers;

    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function customer_validation($scope) {
    $scope.error_message = "";
    $scope.error_flag = false;
    if($scope.customer_name == '') {
        $scope.error_message = "Please enter customer name";
        $scope.error_flag = true;
        return false;
    } else if($scope.email_id != undefined ) {
        if (!validateEmail($scope.email_id)){
            $scope.error_message = "Please enter a valid email id";
            $scope.error_flag = true;
            return false;
        }
    }
    return true;
}

function add_new_customer($http, $scope) {
    $scope.is_valid = customer_validation($scope);
    if ($scope.is_valid) {
        params = { 
            'name': $scope.customer_name,
            'house': $scope.house_name,
            'street': $scope.street,
            'city': $scope.city,
            'district':$scope.district,
            'pin': $scope.pin,
            'mobile': $scope.mobile,
            'phone': $scope.land_line,
            'email': $scope.email_id,
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/create_customer/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.message = data.message;
            } else {
                $scope.customer = data.customer_name;
                $scope.popup.hide_popup();
                get_customers($scope, $http);
                $scope.customer = data.customer_name;
            }
        }).error(function(data, success){
            
        });
    } 
}   

function projectform_validation($scope) {
    $scope.project.start_date = $$('#start_date')[0].get('value');
    $scope.project.end_date = $$('#end_date')[0].get('value');
    if ($scope.project.name == '' || $scope.project.name == undefined) {
        $scope.validation_error = 'Please enter Name';
        return false;
    } else if ($scope.project.start_date == '' || $scope.project.start_date == undefined) {
        $scope.validation_error = 'Please choose Start Date';
        return false;
    } else if ($scope.project.end_date == '' || $scope.project.end_date == undefined) {
        $scope.validation_error = 'Please choose End Date';
        return false;
    } else if ($scope.project.budget_amount != Number($scope.project.budget_amount)) {
        $scope.validation_error = 'Please enter valid Budjet Amount';
        return false;
    }
    return true;
}

function create_project($scope, $http, from) {
    $scope.is_valid = projectform_validation($scope);
    params = {
        'csrfmiddlewaretoken': $scope.csrf_token,
        'project_details': angular.toJson($scope.project),
    }
    if ($scope.is_valid) {
        $http({
            method : 'post',
            url : "/project/create_project/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
            } else {
                $scope.error_flag=false;
                $scope.message = '';
                if (from == 'purchase') {
                    $scope.close_popup();
                    get_projects($scope, $http, 'purchase');
                    $scope.purchase.project_id = data.id
                } else {
                    document.location.href ='/project/projects/';
                }
            }
        }).error(function(data, status){
            console.log(data);
        });
    }
}    

function get_expense_head_list($scope, $http) {
    $http.get('/expenses/expense_head_list/').success(function(data)
    {
        $scope.expense_heads = data.expense_heads;
        $scope.expense_head = 'select';
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function get_dn_details($scope, $http, from) {
    if (from == 'dn_sales' || from == 'print') {
        $scope.dn_no = $scope.dn_no;
    } else {
        $scope.dn_no = $scope.delivery_note_no;
    }

    var url = '/sales/dn_details/?dn_no='+$scope.dn_no;

    $http.get(url).success(function(data)
    {
        if (from == 'print') {
            if (data.whole_delivery_notes.length == 0) {
                $scope.dn_message = 'No Delivery Note with this Delivery no';
                $scope.delivery_note = {
                    'date': '',
                    'id': '',
                    'dn_no': '',
                    'lpo_no': '',
                    'project_name': '',
                    'sales_items': '',
                    'net_total': '',
                    'customer': '',
                }
            } else {
                $scope.dn_message = '';
                $scope.delivery_note = data.whole_delivery_notes[0];
                $scope.dn_id = $scope.delivery_note.id;
            }
        } else {
            if (data.delivery_notes.length == 0) {
                $scope.dn_message = 'No Delivery Note with this Delivery no';
                $scope.delivery_note_selected = true;
                $scope.delivery_note = {
                    'id': [],
                    'dn_no': '',
                    'lpo_no':'',
                    'project_name': '',
                    'project_id': '',
                    'sales_items': '',
                    'date': '',
                    'customer': '',
                    'net_total': 0,
                    'is_project': '',
                    'removed_items': [],
                }
            } else {
                $scope.dn_message = '';
                $scope.delivery_note = data.delivery_notes[0];
                $scope.delivery_note.removed_items = [];
            }
        }
        
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function get_sales_invoice_details($scope, $http, from) {
    $scope.invoice_message = '';
        
    var invoice_no = $scope.invoice_no;
    

    $http.get('/sales/invoice_details/?invoice_no='+invoice_no).success(function(data)
    {
        if (from == 'sales') {
            $scope.sales = {
                'invoice_no': '',
                'project_name': '',
                'delivery_note_no': '',
                'sales_items': [],
                'removed_items': [],
                'customer': '', 
                'date': '',
                'lpo_number': '',
                'total_amount': '',
                'salesman': '',
                'payment_mode': 'cash',
                'cheque_no': '',
                'bank_name': '',
                'branch': '',
                'cheque_date': '',
                'bank_name': '',
                'net_total': '',
                'net_discount': '',
                'roundoff': 0,
                'grant_total': '',
                'paid': 0,
                'balance': 0,
                'id': '',
                'balance_payment':0,
                'paid_amount': 0,
                'discount_sale': 0,
                'discount_sale_percentage': 0,
            } 
            if(data.sales_invoices.length > 0){
                $scope.message = '';
               
                $scope.sales = data.sales_invoices[0]; 
                $scope.payment_mode_change_sales($scope.sales.payment_mode);
                $scope.sales.balance_payment = $scope.sales.balance;
                $scope.sales.paid_amount = $scope.sales.paid;
                $scope.sales.paid = 0;
                $scope.sales.removed_items = [];
            } else {
                $scope.message = "There is no invoice with this number";
            }
        } else if (from == 'print') {
            $scope.add_invoice = function(invoice) {
        $scope.sales = invoice;
        $scope.invoice_no = invoice.invoice_no;
        $scope.invoice_selected = true;
        
    }
            if(data.whole_invoices.length > 0){
                $scope.invoice_message = '';
                $scope.sales = data.whole_invoices[0]; 
                $scope.sales_id = $scope.sales.id;
            } else {
                $scope.invoice_message = "There is no invoice with this number";
            }
        } else {
            if(data.rv_invoice_details.length > 0){
                $scope.selecting_invoice = true;
                $scope.invoice_selected = false;
                $scope.invoices = data.rv_invoice_details; 
            } else {
                $scope.invoice_message = "There is no invoice with this number";
            }
        }
        
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function check_delivery_note_exists($scope, $http) {
    var delivery_note_no = $scope.delivery_note.delivery_note_number;
    $http.get('/sales/check_delivery_note_no_existence/?delivery_no='+delivery_note_no).success(function(data)
    {
        if(data.result == 'error') {
            $scope.existance_message = 'Delivery Note with this no already exists';
            $scope.delivery_note_existing = true;
        } else {
            $scope.existance_message = '';
            $scope.delivery_note_existing = false;
        }  
    });
}

function check_sales_invoice_no_exists($scope, $http) {
    var sales_invoice_no = $scope.sales.sales_invoice_number;
    $http.get('/sales/check_invoice_no_existence/?invoice_no='+sales_invoice_no).success(function(data)
    {
        if(data.result == 'error') {
            $scope.existance_message = 'Sales Invoice with this no already exists';
            $scope.sales_invoice_existing = true;
        } else {
            $scope.existance_message = '';
            $scope.sales_invoice_existing = false;
        }  
    });
}
function get_service_charges($scope, $http, parameter, param){
    $http.get('/project/service_charges/?'+parameter+'='+param).success(function(data)
    {
        if (data.service_charges.length == 0) {
            $scope.sc_item_select_error = 'Service charge not found';
        } else {
            $scope.sc_item_select_error = '';
            $scope.sc_selecting_item = true;
            $scope.sc_item_selected = false;
            $scope.sc_items = data.service_charges;
        }
        
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}


/****************** End Common JS Methods ****************************/

function CreateProjectController($scope, $element, $http, $timeout, $location) {
    $scope.project = {
        'id': '',
        'name': '',
        'start_date': '',
        'end_date': '',
        'budget_amount': 0,
    }
    $scope.init = function(csrf_token, project_id) {
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        if (project_id) {
            $http.get("/project/create_project/?project_id="+project_id).success(function(data)
            {
                $scope.project.id = data.project.id;
                $scope.project = data.project[0];
                console.log(data.project[0]);
            }).error(function(data, status){
            
                console.log(data || "Request failed");
            });
        }

    }
    $scope.create_project = function() {
        create_project($scope, $http, '');
    }
}

function PurchaseController($scope, $element, $http, $timeout, share, $location) {
    $scope.item = {
        'name': '',
        'code': '',
    }
    $scope.item_name = 'select';

    $scope.selected_item = '';
    $scope.supplier_name = '';
    $scope.company_name = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.payment_cheque = true;
    $scope.purchase = {
        'purchase_items': [],
        'purchase_invoice_number': '',
        'supplier_invoice_number': '',
        'supplier_do_number': '',
        'supplier_invoice_date': '',
        'purchase_invoice_date': '',
        'supplier_name': '',
        'transport': '',
        'discount': 0,
        'net_total': 0,
        'purchase_expense': 0,
        'grant_total': 0,
        'supplier_amount': 0,
        'deleted_items': [],
        'payment_mode':'cash',
        'bank_name': '',
        'cheque_no': '',
        'cheque_date': '',
        'discount_percentage': 0,
        'project_id': 'select',
        'purchase_mode':'project_purchase',
    }
    
    $scope.purchase.supplier_name = 'select';
    $scope.purchase.transport = 'select';
    $scope.init = function(csrf_token, invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.purchase.purchase_invoice_number = invoice_number;
        $scope.popup = '';

        new Picker.Date($$('#supplier_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#purchase_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_suppliers($scope, $http);
        get_companies($scope, $http);
        get_items($scope, $http, 'purchase');
        get_projects($scope, $http);
        $scope.purchase.project_id = 'select';
    }
    $scope.payment_mode_change_purchase = function(type) {
        if (type == 'cash' || type == 'credit') {
            $scope.payment_cheque = true;
        } else {
            $scope.payment_cheque = false;
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        }
    }

    $scope.remove_item_purchase_list = function(item) {
        var index = $scope.purchase.purchase_items.indexOf(item);
        $scope.purchase.purchase_items.splice(index, 1);
        $scope.calculate_net_total();
    }

    $scope.add_supplier = function() {
        if($scope.purchase.supplier_name == 'other') {
            $scope.validation_error = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_supplier'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_supplier = function() {
        add_new_supplier($scope, $http);
    }

    $scope.add_transport = function() {
        $scope.message = '';
        if($scope.purchase.transport == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_company'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.add_new_company = function() {
        add_new_company($scope, $http);
    }
    $scope.add_item_to_list = function(item) {
        if ($scope.purchase.project_id == '' || $scope.purchase.project_id == 'select' || $scope.purchase.project_id == 'other') {
            $scope.project_validation_error = 'Please choose Project';
            $scope.item_name = 'select';
        } else {
            $scope.project_validation_error = '';
            if ($scope.purchase.purchase_items.length > 0) {
                for (var i=0;i<$scope.purchase.purchase_items.length; i++) {
                    if ($scope.purchase.purchase_items[i].item_code == item.code) {
                        $scope.item_select_error = 'Item already selected';
                        return false;
                    }
                }
            }
            var selected_item = {
                'item_code': item.code,
                'item_name': item.name,
                'current_stock': item.current_stock,
                'selling_price': 0,
                'qty_purchased': 0,
                'cost_price': 0,
                'net_amount': 0,
                'unit_price': 0,
                'type': item.type,
            }
            $scope.purchase.purchase_items.push(selected_item);
            $scope.item_select_error = '';
        }
        
    } 
    $scope.add_new_item = function() {
        $scope.validation_error = '';

        $scope.item = {
            'name': '',
            'code': '',
        }

        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '384px',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#add_item'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.add_item =  function(){
        add_item($scope, $http, '');
    }
    $scope.add_project = function() {
        $scope.project = {
            'name': '',
            'start_date': '',
            'end_date': '',
            'budget_amount': 0,
        }
        if ($scope.purchase.project_id == 'other') {
            $scope.validation_error = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '384px',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#create_project'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        } else {
            get_items($scope, $http, 'purchase');
        }
    }

    $scope.create_project = function(){
        create_project($scope, $http, 'purchase');
    }
    
    $scope.calculate_cost_price = function(item) {
        if(item.unit_price == '' || item.unit_price != Number(item.unit_price)){
            item.unit_price = 0;
        }
        if(item.unit_price != ''){
            item.cost_price = parseFloat(item.unit_price) 
        }
        $scope.calculate_net_amount(item);
    }

    $scope.calculate_net_amount = function(item) {
        if(item.qty_purchased == '' || item.qty_purchased != Number(item.qty_purchased)) {
            item.qty_purchased = 0;
        }
        if(item.unit_price != Number(item.unit_price)) {
            item.unit_price = 0;
        }
        if(item.qty_purchased != '' && item.unit_price != ''){         
            
            item.net_amount = ((parseFloat(item.qty_purchased)*parseFloat(item.unit_price))).toFixed(2);
        }
        $scope.calculate_supplier_amount();
        $scope.calculate_net_total();
    }

    $scope.calculate_supplier_amount = function() {
        var supplier_amount = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            supplier_amount = supplier_amount + (parseFloat($scope.purchase.purchase_items[i].unit_price)*parseFloat($scope.purchase.purchase_items[i].qty_purchased));
        }

        $scope.purchase.supplier_amount = supplier_amount;
    }

    $scope.calculate_net_total = function(){
        var net_total = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            net_total = net_total + parseFloat($scope.purchase.purchase_items[i].net_amount);
        }
        $scope.purchase.net_total = net_total;
        $scope.calculate_grant_total();
    }

    $scope.calculate_discount_percentage = function() {

        if ($scope.purchase.discount == '' || $scope.purchase.discount != Number($scope.purchase.discount)) {
            $scope.purchase.discount_percentage = 0;
        }
        if ($scope.purchase.net_total == '' || $scope.purchase.net_total != Number($scope.purchase.net_total)) {
            $scope.purchase.discount_percentage = 0;
        }
        $scope.purchase.discount_percentage = ((parseFloat($scope.purchase.discount)/parseFloat($scope.purchase.net_total))*100).toFixed(2);
        $scope.calculate_grant_total();
    }
    $scope.calculate_discount_amount = function() {
        if ($scope.purchase.discount_percentage == '' || $scope.purchase.discount_percentage != Number($scope.purchase.discount_percentage)) {
            $scope.purchase.discount = 0;
        }
        if ($scope.purchase.net_total == '' || $scope.purchase.net_total != Number($scope.purchase.net_total)) {
            $scope.purchase.discount = 0;
        }
        $scope.purchase.discount = ((parseFloat($scope.purchase.discount_percentage) * parseFloat($scope.purchase.net_total))/100).toFixed(2);
        $scope.calculate_grant_total();
    }
    $scope.calculate_grant_total = function(){
        $scope.purchase.grant_total = $scope.purchase.net_total - $scope.purchase.discount;
        $scope.purchase.supplier_amount = $scope.purchase.net_total - $scope.purchase.discount;
    }
    $scope.validate_purchase = function() {
        $scope.purchase.purchase_invoice_date = $$('#purchase_invoice_date')[0].get('value');
        $scope.purchase.supplier_invoice_date = $$('#supplier_invoice_date')[0].get('value');
        if($$('#cheque_date').length > 0)
            $scope.purchase.cheque_date = $$('#cheque_date')[0].get('value');
        $scope.validation_error = '';
        if($scope.purchase.supplier_invoice_number == '') {
            $scope.validation_error = "Please enter Supplier invoice number" ;
            return false;
        } else if($scope.purchase.supplier_do_number == ''){
            $scope.validation_error = "Please enter Supplier D.O number";
            return false;
        } else if($scope.purchase.supplier_invoice_date == '') {
            $scope.validation_error = "Please enter Supplier invoice date";
            return false;
        } else if($scope.purchase.purchase_invoice_date == ''){
            $scope.validation_error = "Please enter purchase invoice date";
            return false;
        } else if($scope.purchase.supplier_name == 'select') {
            $scope.validation_error = "Please select supplier";
            return false;
        } else if($scope.purchase.project_id == 'select') {
            $scope.validation_error = "Please select Project";
            return false;
        } else if($scope.payment_mode == '') {
            $scope.validation_error = "Please choose Payment mode";
            return false;
        } else if(!$scope.payment_cheque && $scope.purchase.bank_name == '') {
            $scope.validation_error = "Please enter Bank name";
            return false;
        } else if (!$scope.payment_cheque && $scope.purchase.cheque_no == '') {
            $scope.validation_error = "Please enter Cheque no.";
            return false;
        } else if (!$scope.payment_cheque && $scope.purchase.cheque_date == '') {
            $scope.validation_error = "Please choose Cheque date";
            return false;
        } else if($scope.purchase.purchase_items.length == 0){
            $scope.validation_error = "Please Choose Item";
            return false;
        } else if(!(Number($scope.purchase.purchase_invoice_number) == $scope.purchase.purchase_invoice_number)) {
            
            $scope.validation_error = "Please enter a number as purchase invoice number";
            return false;
        } else if(!(Number($scope.purchase.discount) == $scope.purchase.discount)) {
            $scope.validation_error = "Please enter a number as discount";
        } else if ($scope.purchase.purchase_items.length > 0) {
            for(i=0; i<$scope.purchase.purchase_items.length; i++){
                if ($scope.purchase.purchase_items[i].selling_price == 0 || $scope.purchase.purchase_items[i].selling_price == '') {
                    $scope.validation_error = "Enter selling price for the item with code "+$scope.purchase.purchase_items[i].item_code;
                    return false;
                } else if ($scope.purchase.purchase_items[i].unit_price == 0 || $scope.purchase.purchase_items[i].unit_price == '') {
                    $scope.validation_error = "Enter unit price for the item with code "+$scope.purchase.purchase_items[i].item_code;
                    return false;
                } else if ($scope.purchase.purchase_items[i].qty_purchased == 0 || $scope.purchase.purchase_items[i].qty_purchased == '') {
                    $scope.validation_error = "Enter quantity purchased for the item with code "+$scope.purchase.purchase_items[i].item_code;
                    return false;
                }
            }
        }
        return true;
    }

    $scope.save_purchase = function() {
        if($scope.validate_purchase()) {
            params = { 
                'purchase': angular.toJson($scope.purchase),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/purchase/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/entry/?purchase_type=project_based';
               
            }).error(function(data, success){
                
            });
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
}

function SalesController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.customer = 'select';
    $scope.customer_name = '';
    $scope.payment_cheque = true;
    $scope.item_name = '';
    $scope.sales = {
        'sales_items': [],
        'project_id': 'select',
        'sales_invoice_number': '',
        'date_sales': '',
        'customer':'',
        'net_total': 0,
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'bank_name': '',
        'branch': '',
        'cheque_no': '',
        'payment_mode': 'cash',
        'paid': 0,
        'balance': 0,
        'discount': 0,
        'discount_percentage': 0,
        'sales_mode':'project_direct',
        'removed_items': [],
        'po_no': '',
        'terms': '',
        'rep': '',
        'via': '',
        'fob': '',
        
    }
    $scope.sales.customer = 'select';
    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.sales.sales_invoice_number = sales_invoice_number;
        $scope.popup = '';
        get_customers($scope, $http);
        get_items($scope, $http, 'sales');
        get_projects($scope, $http);

        var date_picker = new Picker.Date($$('#sales_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });

    }

    $scope.get_service_charge = function(parameter) {
        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.sc_item_code;
        else if(parameter == 'item_name')
            var param = $scope.sc_item_name;
        if($scope.sc_item_code == '' && $scope.sc_item_name == '') {
            $scope.sc_items = [];
            return false;
        }
        get_service_charges($scope, $http, parameter, param);
    }

    $scope.add_sc_item = function(item) {
        $scope.sc_item_selected = true;
        $scope.project_validation_error = '';
        if($scope.sales.sales_items.length > 0) {
            for(var i=0; i<$scope.sales.sales_items.length; i++) {
                if ($scope.sales.sales_items[i].item_code == item.code) {
                    $scope.item_select_error = 'Item already selected';
                    return false;
                }

            }
        }
        var selected_item = {
            'item_code': item.code,
            'item_name': item.name,
            'current_stock': item.current_stock,
            'unit_price': item.unit_price,
            'net_amount': 0,
            'qty_sold': 0,
            'type': item.type,
        }
        $scope.sales.sales_items.push(selected_item);
        $scope.item_select_error = '';
    }

    $scope.is_sales_invoice_exists = function() {
        check_sales_invoice_no_exists($scope, $http);
    }

    $scope.add_item_to_list = function(item) {
        $scope.item_selected = true;
        if ($scope.sales.project_id == '' || $scope.sales.project_id == 'select' || $scope.sales.project_id == 'other') {
            $scope.project_validation_error = 'Please choose Project';
            $scope.item_name = 'select';
        } else {
            $scope.project_validation_error = '';
            if($scope.sales.sales_items.length > 0) {
                for(var i=0; i<$scope.sales.sales_items.length; i++) {
                    if ($scope.sales.sales_items[i].item_code == item.code) {
                        $scope.item_select_error = 'Item already selected';
                        return false;
                    }

                }
            }
            var selected_item = {
                'item_code': item.code,
                'item_name': item.name,
                'current_stock': item.current_stock,
                'unit_price': item.unit_price,
                'net_amount': 0,
                'qty_sold': 0,
                'type': item.type,
            }
            $scope.sales.sales_items.push(selected_item);
            $scope.item_select_error = '';
        }
        
    } 

    $scope.payment_mode_change_sales = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_cheque = false;
            
            var date_picker = new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
                
        } else {
            $scope.payment_cheque = true;
        }
    }
    $scope.validate_sales = function() {
        $scope.sales.customer = $scope.customer;
        $scope.sales.sales_invoice_date = $$('#sales_invoice_date')[0].get('value');
        $scope.sales.cheque_date = $$('#cheque_date')[0].get('value');
        if($scope.sales.sales_invoice_date == '') {
            $scope.validation_error = "Enter Sales invoice Date" ;
            return false;
        } else if($scope.sales.sales_invoice_number == '' || $scope.sales.sales_invoice_number == undefined) {
            $scope.validation_error = "Enter Invoice no" ;
            return false;
        } else if($scope.sales.customer =='select'){
            $scope.validation_error = "Choose Customer";
            return false;
        } else if($scope.sales.sales_invoice_number == '' || $scope.sales.sales_invoice_number == undefined) {
            $scope.validation_error = "Enter Sales invoice no" ;
            return false;
        } else if($scope.sales.project_id =='select') {
            $scope.validation_error = "Choose Project";
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.bank_name == '' || $scope.sales.bank_name == undefined)){
            $scope.validation_error = "Please enter Bank Name";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.branch == '' || $scope.sales.branch == undefined)){
            $scope.validation_error = "Please enter Branch";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.cheque_no == '' || $scope.sales.cheque_no == undefined)){
            $scope.validation_error = "Please enter Cheque No.";
            return false;
        } else if(!$scope.payment_cheque && ($scope.sales.cheque_date == '' || $scope.sales.cheque_date == undefined)){
            $scope.validation_error = "Please enter Cheque Date.";
            return false;
        } else if ($scope.sales.paid == 0 && $scope.sales.payment_mode == 'cash') {
            $scope.validation_error ="You have choosed cash as payment mode , so please enter the PAID";
            return false;
        } else if ((parseFloat($scope.sales.paid) != parseFloat($scope.sales.grant_total)) && ($scope.sales.payment_mode == 'cash' || $scope.sales.payment_mode == 'cheque')) {
            $scope.validation_error ="Please choose payment mode as credit , because you have balance amount.";
            return false;
        } else if($scope.sales.sales_items.length > 0){
            for (var i=0; i < $scope.sales.sales_items.length; i++){
                if ($scope.sales.sales_items[i].type == 'item' && parseInt($scope.sales.sales_items[i].current_stock) < parseInt($scope.sales.sales_items[i].qty_sold)){
                    $scope.validation_error = "Quantity not in stock for item with code "+$scope.sales.sales_items[i].item_code;
                    return false;
                }
            }
        } 
        return true;
    }

    $scope.get_items = function(parameter) {
        if ($scope.sales.project_id == 'select' || $scope.sales.project_id == '' ||  $scope.sales.project_id == undefined) {
            $scope.item_select_error = ' Please Choose the project';
        } else {
            $scope.item_select_error = '';
            if(parameter == 'item_code')
                var param = $scope.item_code;
            else if(parameter == 'item_name')
                var param = $scope.item_name;
            if($scope.item_code == '' && $scope.item_name == '') {
                $scope.items = [];
                return false;
            }
            get_project_items($scope, $http, parameter, param, 'sales');
        }
    }

    $scope.add_customer = function() {
        $scope.name = '';
        $scope.house = '';
        $scope.street = '';
        $scope.city = '';
        $scope.district = '';
        $scope.pin = '';
        $scope.mobile = '';
        $scope.phone = '';
        $scope.email = '';
        if($scope.customer == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
        
       add_new_customer($http, $scope);
    }

    $scope.items = [];
    $scope.sales_items = [];
    
    $scope.getItems = function(){
        get_items($scope, $http, 'sales')
    }

    $scope.calculate_net_total_sale = function() {
        net_total = 0
        for (var i=0; i < $scope.sales.sales_items.length; i++ ){
            net_total = parseFloat(net_total) + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
    }

    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if (!Number(item.qty_sold) || item.qty_sold == '' || item.qty_sold == undefined) {
            item.qty_sold = 0
        }
        if(item.type == 'item' && parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Quantity for the item with code "+ item.item_code+ " not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            }
            $scope.calculate_net_total_sale();
        }
    }

    $scope.calculate_discount_percentage = function() {

        if ($scope.sales.discount == '' || !Number($scope.sales.discount)) {
            $scope.sales.discount = 0;
            $scope.sales.discount_percentage = 0;
        }
        if ($scope.sales.net_total == '' || !Number($scope.sales.net_total)) {
            $scope.sales.discount_percentage = 0;
        }
        $scope.sales.discount_percentage = ((parseFloat($scope.sales.discount)/parseFloat($scope.sales.net_total))*100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }
    $scope.calculate_discount_amount = function() {
        if ($scope.sales.discount_percentage == '' || !Number($scope.sales.discount_percentage)) {
            $scope.sales.discount = 0;
            $scope.sales.discount_percentage = 0;
        }
        if ($scope.sales.net_total == '' || !Number($scope.sales.net_total)) {
            $scope.sales.discount = 0;
        }
        $scope.sales.discount = ((parseFloat($scope.sales.discount_percentage) * parseFloat($scope.sales.net_total))/100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }

    $scope.calculate_grant_total_sale = function(){
        if ($scope.sales.net_total == '' || $scope.sales.net_total == undefined || !Number($scope.sales.net_total)){
            $scope.sales.net_total = 0;
        }
        if ($scope.sales.roundoff == '' || $scope.sales.roundoff == undefined || !Number($scope.sales.roundoff)){
            $scope.sales.roundoff = 0;
        }
        if ($scope.sales.discount == '' || $scope.sales.discount == undefined || !Number($scope.sales.discount)){
            $scope.sales.discount = 0;
        }
        $scope.sales.grant_total = (parseFloat($scope.sales.net_total) - (parseFloat($scope.sales.roundoff) + parseFloat($scope.sales.discount))).toFixed(2);
        $scope.calculate_balance_sale();
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = $scope.sales.grant_total - $scope.sales.paid;
    }
    $scope.remove_from_item_list = function(item) {
        var index = $scope.sales.sales_items.indexOf(item);
        $scope.sales.sales_items.splice(index, 1);
        $scope.calculate_net_total_sale();
    }
    $scope.save_sales = function() {

        if($scope.validate_sales()){
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/invoice_pdf/'+data.id+'/';                
            }).error(function(data, success){
                
            });
        }          
    }
}

function ReceiptVoucherController($scope, $element, $http, $location) {

    $scope.receiptvoucher = {
        'customer': '',
        'payment_mode': 'cash',
        'bank_name': '',
        'receipt_voucher_date': '',
        'cheque_no': '',
        'cheque_date': '',
        'amount': '',
        'invoice_no': '',
        'voucher_no': '',
        'paid_amount': 0,

    }
    $scope.receiptvoucher.customer = '';
    $scope.receiptvoucher.receipt_voucher_date = '';
    $scope.receiptvoucher.cheque_no = '';
    $scope.receiptvoucher.cheque_date = '';
    $scope.receiptvoucher.payment_mode = 'cash';
    $scope.cash = 'true';

    $scope.init = function(csrf_token, voucher_no) {
        $scope.csrf_token = csrf_token;
        $scope.receiptvoucher.voucher_no = voucher_no;

        $scope.date_picker_cheque = new Picker.Date($$('#cheque_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
        $scope.date_picker_cheque = new Picker.Date($$('#receipt_voucher_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
    }

    $scope.is_rv_exists = function() {
        
        var rv_no = $scope.receiptvoucher.voucher_no;
        $http.get('/sales/check_receipt_voucher_existence/?rv_no='+rv_no).success(function(data)
        {
            if(data.result == 'error') {
                $scope.existance_message = 'Receipt Voucher with this no already exists';
                $scope.rv_existing = true;
            } else {
                $scope.existance_message = '';
                $scope.rv_existing = false;
            }  
        });
    }
    
    $scope.receipt_validation = function(){

        $scope.receiptvoucher.date = $$('#receipt_voucher_date')[0].get('value');
        $scope.receiptvoucher.voucher_no = $$('#voucher_no')[0].get('value');
        var balance_amount = parseFloat($scope.receiptvoucher.amount) - (parseFloat($scope.receiptvoucher.paid) + parseFloat($scope.receiptvoucher.paid_amount));
        if ($scope.receiptvoucher.invoice_no == '' || $scope.receiptvoucher.invoice_no == undefined) {
            $scope.validation_error = "Enter the Sales Invoice no.";
            return false;             
        } 
        if (balance_amount < 0 ) {
            $scope.validation_error = "Please enter valid amount on Paid ";
            return false;
        }
        if($scope.receiptvoucher.payment_mode == 'cash') {
            $scope.receiptvoucher.bank_name = '';
            $scope.receiptvoucher.cheque_no = '';
            $scope.receiptvoucher.cheque_date = '';
        } else {
            
            if($scope.receiptvoucher.bank_name =='' || $scope.receiptvoucher.bank_name==undefined){
                $scope.validation_error = "Please enter bank name";
                return false;
            }else if($scope.receiptvoucher.cheque_no == '' || $scope.receiptvoucher.cheque_no == undefined){
                $scope.validation_error = "Please enter cheque no";
                return false;
            }else if($$('#cheque_date')[0].get('value') == ''){
                $scope.validation_error = "Please enter cheque date";
                return false;
            }
            if($$('#cheque_date')[0].get('value') != '') {
                $scope.receiptvoucher.cheque_date = $$('#cheque_date')[0].get('value');
            }
        }        
        return true;
    }

    $scope.get_sales_invoice_details = function(){
        get_sales_invoice_details($scope, $http, 'rv');
    }
    $scope.add_invoice = function(invoice) {
        $scope.selecting_invoice = false;
        $scope.invoice_selected = true;
        $scope.invoice_no = invoice.invoice_no;
        $scope.receiptvoucher.invoice_no =  $scope.invoice_no;
        $scope.receiptvoucher.customer = invoice.customer;
        $scope.receiptvoucher.amount = invoice.amount;
        $scope.receiptvoucher.paid = invoice.paid_amount;
        $scope.balance = parseFloat($scope.receiptvoucher.amount) - parseFloat($scope.receiptvoucher.paid);
    }

    $scope.save_receipt = function(){
        $scope.is_valid = $scope.receipt_validation();
        if ($scope.is_valid) {
            $scope.error_flag = false;
            $scope.error_message = '';
            params = { 
                'receiptvoucher': angular.toJson($scope.receiptvoucher),   
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/receipt_voucher/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href ='/sales/receipt_voucher/';
                }
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
    $scope.payment_mode_change = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.cash = false;
        } else {
            $scope.cash = true;
        }       
    }
}

function ExpenseController($scope, $element, $http, $timeout, $location) {

    $scope.expense =  {
        'expense_head_id': 'select',
        'voucher_no': '',
        'cheque_no': '',
        'cheque_date': '',
        'date': '',
        'payment_mode': 'cash',
        'narration': '',
        'project_id': 'select',
        'branch': '',
        'bank_name': '',
        'amount': 0,
    }
    $scope.expense_heads = [];
    $scope.expense_head = '';
    
    $scope.payment_mode_selection = true;
    $
    $scope.is_valid = false;
    $scope.error_flag = false;
    $scope.error_message = '';

    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        get_expense_head_list($scope, $http);
        get_projects($scope, $http);
    }
    $scope.payment_mode_change = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_mode_selection = false;
            
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        } else {
            $scope.payment_mode_selection = true;
        }
    }

    $scope.add_expense_head = function() {
        $scope.head_name = '';
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '36%',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#add_expense_head'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_head = function(){
        if ($scope.head_name == '' || $scope.head_name == undefined) {
            $scope.message = 'Please enter Head Name';
        } else {
            $scope.message = '';
            params = { 
                'head_name': $scope.head_name,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expenses/new_expense_head/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                if (data.result == 'error') {
                    $scope.message = data.message;
                } else {
                    $scope.message = '';
                    get_expense_head_list($scope, $http);
                    $scope.expense.expense_head_id = data.head_id;
                    $scope.close_popup();
                }
                
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
    
    $scope.form_validation = function(){
        $scope.expense.voucher_no = $$('#voucher_no')[0].get('value');
        $scope.expense.date = $$('#date')[0].get('value');
        $scope.expense.cheque_date = $$('#cheque_date')[0].get('value');

        if ($scope.expense.expense_head_id == '' || $scope.expense.expense_head_id == undefined || $scope.expense.expense_head_id == 'select') {
            $scope.error_flag = true;
            $scope.error_message = 'Please choose Expense Head';
            return false;
        } else if ($scope.expense.amount == '' || $scope.expense.amount == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please enter amount';
            return false;
        } else if ($scope.expense.narration == '' || $scope.expense.narration == undefined) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add narration';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.cheque_no == '' || $scope.expense.cheque_no == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque no';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.cheque_date == '' || $scope.expense.cheque_date == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add cheque date';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.bank_name == '' || $scope.expense.bank_name == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add bank name';
            return false;
        } else if( $scope.expense.payment_mode == 'cheque' && ($scope.expense.branch == '' || $scope.expense.branch == undefined)) {
            $scope.error_flag = true;
            $scope.error_message = 'Please add branch';
            return false;
        }
        return true;
    }
    $scope.save_expense = function(){
        if ($scope.form_validation()) {
            $scope.error_flag = false;
            $scope.error_message = '';
            params = { 
                'expense': angular.toJson($scope.expense),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/expenses/new_expense/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href ='/expenses/new_expense/';
                }
            }).error(function(data, status){
                console.log(data);
            });
        }
    }
}

function PurchaseReportController($scope, $http, $location) {
    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
        $scope.project_name = 'select';
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
}

function ExpenseReportController ($scope, $http) {
    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
        $scope.project_name = 'select';
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        get_expense_head_list($scope, $http);
    }
}

function WholeSalesReportController($scope, $http) {
    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }
}
function SalesReportController($scope, $http, $location) {
    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
        $scope.project_name = 'select';
        $scope.report_type = 'select';
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        if (report_type == 'date_based') {
            $scope.report_type = report_type;
            $scope.date_based = true;
            $scope.project_based = false;
        } else if (report_type == 'project_based') {
            $scope.report_type = report_type;
            $scope.date_based = false;
            $scope.project_based = true;
        }
    }
    $scope.get_report_type = function(){
        if ($scope.report_type == 'date_based') {
            $scope.date_based = true;
            $scope.project_based = false;
        } else if ($scope.report_type == 'project_based') {
            $scope.date_based = false;
            $scope.project_based = true;
        }
    }
}

function CashReportController($scope, $http, $location) {

    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
        $scope.project_name = 'select';
    }

}
function BankIncomeReportController($scope, $http, $location) {

    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
        $scope.project_name = 'select'; 
    }
}

function ProjectReportController($scope, $http, $location){
    $scope.init = function(csrf_token, report_type) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
        $scope.project_name = 'select';
    }
}

function DailyReportController($scope, $element, $http, $timeout, $location){ 

    $scope.init = function(){ 
        $scope.error_flag = false;      
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }   

}
function ProjectDeliveryNoteController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.customer = 'select';
    $scope.customer_name = '';
    $scope.item_name = '';
    $scope.delivery_note = {
        'sales_items': [],
        'project_id': 'select',
        'delivery_note_number': '',
        'customer':'',
        'date': 0,
        'lpo_no': 0,
        'net_total': 0,
        'dn_mode': 'project_based',
    }
    $scope.delivery_note.customer = 'select';
    $scope.init = function(csrf_token, delivery_note_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.delivery_note.delivery_note_number = delivery_note_number;
        $scope.popup = '';
        get_customers($scope, $http);
        get_items($scope, $http, 'dn');
        get_projects($scope, $http);
        new Picker.Date($$('#delivery_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }

    $scope.get_items = function(parameter) {
        if ($scope.delivery_note.project_id == 'select' || $scope.delivery_note.project_id == '' ||  $scope.delivery_note.project_id == undefined) {
            $scope.item_select_error = ' Please Choose the project';
        } else {
            $scope.item_select_error = '';
            if(parameter == 'item_code')
                var param = $scope.item_code;
            else if(parameter == 'item_name')
                var param = $scope.item_name;
            if($scope.item_code == '' && $scope.item_name == '') {
                $scope.items = [];
                return false;
            }
            get_project_items($scope, $http, parameter, param, 'dn');
        }
    }

    $scope.get_service_charge = function(parameter) {
        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.sc_item_code;
        else if(parameter == 'item_name')
            var param = $scope.sc_item_name;
        if($scope.sc_item_code == '' && $scope.sc_item_name == '') {
            $scope.sc_items = [];
            return false;
        }
        get_service_charges($scope, $http, parameter, param);
    }

    $scope.add_sc_item = function(item) {
        $scope.sc_item_selected = true;
        $scope.project_validation_error = '';
        if($scope.delivery_note.sales_items.length > 0) {
            for(var i=0; i<$scope.delivery_note.sales_items.length; i++) {
                if ($scope.delivery_note.sales_items[i].item_code == item.code) {
                    $scope.item_select_error = 'Item already selected';
                    return false;
                }

            }
        }
        var selected_item = {
            'item_code': item.code,
            'item_name': item.name,
            'current_stock': item.current_stock,
            'unit_price': item.unit_price,
            'net_amount': 0,
            'qty_sold': 0,
            'type': item.type,
        }
        $scope.delivery_note.sales_items.push(selected_item);
        $scope.item_select_error = '';
    }

    $scope.is_delivery_note_exists = function() {
        check_delivery_note_exists($scope, $http);
    }

    $scope.add_item_to_list = function(item) {
        $scope.item_selected = true;
        if ($scope.delivery_note.project_id == '' || $scope.delivery_note.project_id == 'select' || $scope.delivery_note.project_id == 'other') {
            $scope.project_validation_error = 'Please choose Project';
            $scope.item_name = 'select';
        } else {
            $scope.project_validation_error = '';
            if($scope.delivery_note.sales_items.length > 0) {
                for(var i=0; i< $scope.delivery_note.sales_items.length; i++) {
                    if($scope.delivery_note.sales_items[i].item_code == item.code) {
                        $scope.item_select_error = "Item already selected";
                        return false;
                    }
                }
            } 
            var selected_item = {
                'item_code': item.code,
                'item_name': item.name,
                'current_stock': item.current_stock,
                'unit_price': item.unit_price,
                'net_amount': 0,
                'qty_sold': 0,
                'type': item.type,
            }
            $scope.delivery_note.sales_items.push(selected_item);
            $scope.item_select_error = '';
        }
    } 

    $scope.validate_project_dn = function() {
        $scope.delivery_note.customer = $scope.customer;
        $scope.delivery_note.delivery_note_number = $$('#delivery_note_no')[0].get('value');
        $scope.delivery_note.date = $$('#delivery_date')[0].get('value');
        if($scope.delivery_note.delivery_note_number =='' || $scope.delivery_note.delivery_note_number == undefined ){
            $scope.validation_error = "Enter Delivery Note Number";
            return false;
        } else if($scope.delivery_note.customer =='' || $scope.delivery_note.customer == undefined || $scope.delivery_note.customer =='select'){
            $scope.validation_error = "choose customer";
            return false;
        } else if($scope.delivery_note.lpo_no =='' || $scope.delivery_note.lpo_no == undefined){
            $scope.validation_error = "enter lpo no";
            return false;
        } else if($scope.delivery_note.project_id =='select') {
            $scope.validation_error = "Choose Project";
            return false;
        } else if($scope.delivery_note.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if($scope.delivery_note.sales_items.length > 0){
            for (var i=0; i < $scope.delivery_note.sales_items.length; i++){
                if ($scope.delivery_note.sales_items[i].item_type == 'item' && parseInt($scope.delivery_note.sales_items[i].current_stock) < parseInt($scope.delivery_note.sales_items[i].qty_sold)){
                    $scope.validation_error = "Quantity not in stock for item with code "+$scope.delivery_note.sales_items[i].item_code;
                    return false;
                }
            }
        } 
        return true;
    }

    $scope.add_project = function() {
        get_items($scope, $http, 'dn');
    }

    $scope.add_customer = function() {
        $scope.name = '';
        $scope.house = '';
        $scope.street = '';
        $scope.city = '';
        $scope.district = '';
        $scope.pin = '';
        $scope.mobile = '';
        $scope.phone = '';
        $scope.email = '';
        if($scope.customer == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
       add_new_customer($http, $scope);
    }

    $scope.items = [];
    $scope.sales_items = [];
    
    $scope.getItems = function(){
        get_items($scope, $http, 'dn')
    }

    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if (!Number(item.qty_sold) || item.qty_sold == '' || item.qty_sold == undefined) {
            item.qty_sold = 0
        }
        if( item.item_type == 'item' && parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Quantity for the item with code "+ item.item_code+ " not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            }
        }
        $scope.calculate_net_total_sale();
    }

    $scope.calculate_net_total_sale = function() {
        net_total = 0
        for (var i=0; i < $scope.delivery_note.sales_items.length; i++ ){
            net_total = parseFloat(net_total) + parseFloat($scope.delivery_note.sales_items[i].net_amount);
        }
        $scope.delivery_note.net_total = net_total;
    }

    $scope.remove_from_item_list = function(item) {
        var index = $scope.delivery_note.sales_items.indexOf(item);
        $scope.delivery_note.sales_items.splice(index, 1);
        $scope.calculate_net_total_sale();
    }
    $scope.save_delivery_note = function() {

        if($scope.validate_project_dn()){
            params = { 
                'delivery_note': angular.toJson($scope.delivery_note),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/create_delivery_note/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/delivery_note_pdf/'+data.id+'/';                
            }).error(function(data, success){
                
            });
        }          
    }
}

function SalesDNController($scope, $http, $element, $location) {
    $scope.sales = {
        'sales_items': [],
        'dn_id': '',
        'sales_invoice_number': '',
        'date_sales': '',
        'customer':'',
        'net_total': 0,
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'bank_name': '',
        'branch': '',
        'cheque_no': '',
        'payment_mode': 'cash',
        'paid': 0,
        'balance': 0,
        'discount': 0,
        'discount_percentage': 0,
        'sales_mode':'dn_sales',
        'removed_items': [],
        'po_no': '',
        'terms': '',
        'rep': '',
        'via': '',
        'fob': '',
    }
    $scope.delivery_note = {
        'date': '',
        'lpo_no': '',
        'sales_items': [],
        'net_total':0,
        'customer': '',
        'id': '',
    }
    $scope.payment_cheque = true;
    $scope.init = function(csrf_token, invoice_no) {
        $scope.sales.sales_invoice_number = invoice_no;
        $scope.csrf_token = csrf_token;
        new Picker.Date($$('#sales_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.is_sales_invoice_exists = function() {
        check_sales_invoice_no_exists($scope, $http);
    }
    $scope.get_delivery_note_details = function() {
        $scope.sales.dn_id = '';
        get_dn_details($scope, $http, 'dn_sales');
    }
    $scope.add_delivery_note = function(delivery_note) {
        $scope.delivery_note = delivery_note;
        $scope.dn_no = delivery_note.dn_no;
        $scope.delivery_note_selected = true;
        $scope.sales.dn_id = delivery_note.id;

        $scope.sales.sales_items = [];
        for (var i = 0; i < delivery_note.sales_items.length; i++) {
            var selected_item = {
                'sl_no': delivery_note.sales_items[i].sl_no,
                'item_code': delivery_note.sales_items[i].code,
                'item_name': delivery_note.sales_items[i].name,
                'qty_sold': delivery_note.sales_items[i].qty_sold,
                'current_stock': delivery_note.sales_items[i].current_stock,
                'unit_price': delivery_note.sales_items[i].selling_price,
                'net_amount': delivery_note.sales_items[i].net_amount,
                'dn_item_id': delivery_note.sales_items[i].id,
                'sold_qty': delivery_note.sales_items[i].qty_sold,
                'type': delivery_note.sales_items[i].type,
            }
            $scope.sales.sales_items.push(selected_item);
        }
        $scope.sales.net_total = delivery_note.net_total;
        $scope.calculate_grant_total_sale();
       
    }
    $scope.calculate_grant_total_sale = function(){
        if ($scope.sales.net_total == '' || $scope.sales.net_total == undefined || !Number($scope.sales.net_total)){
            $scope.sales.net_total = 0;
        }
        if ($scope.sales.roundoff == '' || $scope.sales.roundoff == undefined || !Number($scope.sales.roundoff)){
            $scope.sales.roundoff = 0;
        }
        if ($scope.sales.discount == '' || $scope.sales.discount == undefined || !Number($scope.sales.discount)){
            $scope.sales.discount = 0;
        }
        $scope.sales.grant_total = (parseFloat($scope.sales.net_total) - (parseFloat($scope.sales.roundoff) + parseFloat($scope.sales.discount))).toFixed(2);
        $scope.calculate_balance_sale();
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = $scope.sales.grant_total - $scope.sales.paid;
    }
    $scope.remove_from_item_list = function(item) {
        var index = $scope.sales.sales_items.indexOf(item);
        $scope.sales.sales_items.splice(index, 1);
        $scope.sales.removed_items.push(item);
        $scope.calculate_net_total_sale();
    }
    $scope.calculate_net_total_sale = function() {
        net_total = 0
        for (var i=0; i < $scope.sales.sales_items.length; i++ ){
            net_total = parseFloat(net_total) + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
    }
    $scope.calculate_discount_percentage = function() {

        if ($scope.sales.discount == '' || $scope.sales.discount != Number($scope.sales.discount)) {
            $scope.sales.discount_percentage = 0;
        }
        if ($scope.sales.net_total == '' || $scope.sales.net_total != Number($scope.sales.net_total)) {
            $scope.sales.discount_percentage = 0;
        }
        $scope.sales.discount_percentage = ((parseFloat($scope.sales.discount)/parseFloat($scope.sales.net_total))*100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }
    $scope.calculate_discount_amount = function() {
        if ($scope.sales.discount_percentage == '' || $scope.sales.discount_percentage != Number($scope.sales.discount_percentage)) {
            $scope.sales.discount = 0;
        }
        if ($scope.sales.net_total == '' || $scope.sales.net_total != Number($scope.sales.net_total)) {
            $scope.sales.discount = 0;
        }
        $scope.sales.discount = ((parseFloat($scope.sales.discount_percentage) * parseFloat($scope.sales.net_total))/100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }

    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if (!Number(item.qty_sold) || item.qty_sold == '' || item.qty_sold == undefined) {
            item.qty_sold = 0
        }
        if(parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Quantity for the item with code "+ item.item_code+ " not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            }
            $scope.calculate_net_total_sale();
        }
    }
    $scope.payment_mode_change_sales = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_cheque = false;
            
            var date_picker = new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
                
        } else {
            $scope.payment_cheque = true;
        }
    }
    $scope.validate_sales = function() {
        $scope.sales.customer = $scope.customer;
        $scope.sales.sales_invoice_date = $$('#sales_invoice_date')[0].get('value');
        $scope.sales.cheque_date = $$('#cheque_date')[0].get('value');
        if($scope.sales.dn_id == '' || $scope.sales.dn_id == undefined) {
            $scope.validation_error = "Enter Delivery Note No" ;
            return false;
        } else if($scope.sales.sales_invoice_number == '' || $scope.sales.sales_invoice_number == undefined) {
            $scope.validation_error = "Enter Invoice No" ;
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.bank_name == '' || $scope.sales.bank_name == undefined)){
            $scope.validation_error = "Please enter Bank Name";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.branch == '' || $scope.sales.branch == undefined)){
            $scope.validation_error = "Please enter Branch";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.cheque_no == '' || $scope.sales.cheque_no == undefined)){
            $scope.validation_error = "Please enter Cheque No.";
            return false;
        } else if(!$scope.payment_cheque && ($scope.sales.cheque_date == '' || $scope.sales.cheque_date == undefined)){
            $scope.validation_error = "Please enter Cheque Date.";
            return false;
        } else if ($scope.sales.paid == 0 && $scope.sales.payment_mode == 'cash') {
            $scope.validation_error ="You have choosed cash as payment mode , so please enter the PAID";
            return false;
        } else if ((parseFloat($scope.sales.paid) != parseFloat($scope.sales.grant_total)) && ($scope.sales.payment_mode == 'cash' || $scope.sales.payment_mode == 'cheque')) {
            $scope.validation_error ="Please choose payment mode as credit , because you have balance amount.";
            return false;
        } else if($scope.sales.sales_items.length > 0){
            for (var i=0; i < $scope.sales.sales_items.length; i++){
                var newly_purchased = parseInt($scope.sales.sales_items[i].qty_sold) - parseInt($scope.sales.sales_items[i].sold_qty);
                if (parseInt($scope.sales.sales_items[i].current_stock) < parseInt(newly_purchased)) {
                    $scope.validation_error = "Quantity not in stock for item with code "+$scope.sales.sales_items[i].item_code;
                    return false;
                }
            }
        } 
        return true;
    }
    $scope.save_dn_sales = function() {
        if ($scope.validate_sales()){
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/invoice_pdf/'+data.id+'/';                
            }).error(function(data, success){
                
            });
        }
    }
}

function InventoryPurchaseController($scope, $http, $element, $location) {
    $scope.purchase = {
        'purchase_items': [],
        'purchase_invoice_number': '',
        'supplier_invoice_number': '',
        'supplier_do_number': '',
        'supplier_invoice_date': '',
        'purchase_invoice_date': '',
        'supplier_name': 'select',
        'transport': 'select',
        'discount': 0,
        'net_total': 0,
        'purchase_expense': 0,
        'grant_total': 0,
        'supplier_amount': 0,
        'deleted_items': [],
        'payment_mode':'cash',
        'bank_name': '',
        'cheque_no': '',
        'cheque_date': '',
        'discount_percentage': 0,
        'project_id': 'select',
        'purchase_mode':'inventory_purchase',
    }
    $scope.payment_cheque = true;
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.init = function(csrf_token, invoice_number) {
        $scope.csrf_token = csrf_token;
        $scope.purchase.purchase_invoice_number = invoice_number;
        get_companies($scope, $http);
        get_suppliers($scope, $http);
        new Picker.Date($$('#supplier_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#purchase_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.add_transport = function() {
        $scope.message = '';
        if($scope.purchase.transport == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '27%',
                'message_padding': '0px',
                'left': '28%',
                'top': '150px',
                'height': '115px',
                'content_div': '#add_company'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.add_new_company = function() {
        add_new_company($scope, $http);
    }
    $scope.add_supplier = function() {
        if($scope.purchase.supplier_name == 'other') {
            $scope.validation_error = '';
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_supplier'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }

    $scope.add_new_supplier = function() {
        add_new_supplier($scope, $http);
    }
    $scope.payment_mode_change_purchase = function(type) {
        if (type == 'cash' || type == 'credit') {
            $scope.payment_cheque = true;
        } else {
            $scope.payment_cheque = false;
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        }
    }
    $scope.get_items = function(parameter) {

        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        if($scope.item_code == '' && $scope.item_name == '') {
            $scope.items = [];
            return false;
        }
        get_inventory_items($scope, $http, parameter, param);
        
    }
    $scope.add_purchase_item = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.item_select_error = '';
        if($scope.purchase.purchase_items.length > 0) {
            for(var i=0; i< $scope.purchase.purchase_items.length; i++) {
                if($scope.purchase.purchase_items[i].item_code == item.code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {
            'item_code': item.code,
            'item_name': item.name,
            'current_stock': item.current_stock,
            'selling_price': 0,
            'qty_purchased': 0,
            'net_amount': 0,
            'unit_price': 0,
            'cost_price': 0,
            'type': item.type,
        }
        $scope.purchase.purchase_items.push(selected_item);
    }
    $scope.add_new_item = function() {
        $scope.validation_error = '';

        $scope.item = {
            'name': '',
            'code': '',
        }

        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '384px',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#add_item'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.add_item =  function(){
        add_item($scope, $http, '');
    }
    $scope.remove_item_purchase_list = function(item) {
        var index = $scope.purchase.purchase_items.indexOf(item);
        $scope.purchase.purchase_items.splice(index, 1);
        $scope.calculate_net_total();
    }
    $scope.calculate_cost_price = function(item) {
        if(item.unit_price == '' || item.unit_price != Number(item.unit_price)){
            item.unit_price = 0;
        }
        if(item.unit_price != ''){
            item.cost_price = parseFloat(item.unit_price) 
        }
        $scope.calculate_net_amount(item);
    }

    $scope.calculate_net_amount = function(item) {
        if(item.qty_purchased == '' || item.qty_purchased != Number(item.qty_purchased)) {
            item.qty_purchased = 0;
        }
        if(item.unit_price != Number(item.unit_price)) {
            item.unit_price = 0;
        }
        if(item.qty_purchased != '' && item.unit_price != ''){         
            
            item.net_amount = ((parseFloat(item.qty_purchased)*parseFloat(item.unit_price))).toFixed(2);
        }
        $scope.calculate_supplier_amount();
        $scope.calculate_net_total();
    }

    $scope.calculate_supplier_amount = function() {
        var supplier_amount = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            supplier_amount = supplier_amount + (parseFloat($scope.purchase.purchase_items[i].unit_price)*parseFloat($scope.purchase.purchase_items[i].qty_purchased));
        }

        $scope.purchase.supplier_amount = supplier_amount;
    }

    $scope.calculate_net_total = function(){
        var net_total = 0;
        for(i=0; i<$scope.purchase.purchase_items.length; i++){
            net_total = net_total + parseFloat($scope.purchase.purchase_items[i].net_amount);
        }
        $scope.purchase.net_total = net_total;
        $scope.calculate_grant_total();
    }

    $scope.calculate_discount_percentage = function() {

        if ($scope.purchase.discount == '' || $scope.purchase.discount != Number($scope.purchase.discount)) {
            $scope.purchase.discount_percentage = 0;
        }
        if ($scope.purchase.net_total == '' || $scope.purchase.net_total != Number($scope.purchase.net_total)) {
            $scope.purchase.discount_percentage = 0;
        }
        $scope.purchase.discount_percentage = ((parseFloat($scope.purchase.discount)/parseFloat($scope.purchase.net_total))*100).toFixed(2);
        $scope.calculate_grant_total();
    }
    $scope.calculate_discount_amount = function() {
        if ($scope.purchase.discount_percentage == '' || $scope.purchase.discount_percentage != Number($scope.purchase.discount_percentage)) {
            $scope.purchase.discount = 0;
        }
        if ($scope.purchase.net_total == '' || $scope.purchase.net_total != Number($scope.purchase.net_total)) {
            $scope.purchase.discount = 0;
        }
        $scope.purchase.discount = ((parseFloat($scope.purchase.discount_percentage) * parseFloat($scope.purchase.net_total))/100).toFixed(2);
        $scope.calculate_grant_total();
    }
    $scope.calculate_grant_total = function(){
        $scope.purchase.grant_total = $scope.purchase.net_total - $scope.purchase.discount;
        $scope.purchase.supplier_amount = $scope.purchase.net_total - $scope.purchase.discount;
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.validate_purchase = function() {
        $scope.purchase.purchase_invoice_date = $$('#purchase_invoice_date')[0].get('value');
        $scope.purchase.supplier_invoice_date = $$('#supplier_invoice_date')[0].get('value');
        if($$('#cheque_date').length > 0)
            $scope.purchase.cheque_date = $$('#cheque_date')[0].get('value');
        $scope.validation_error = '';
        if($scope.purchase.supplier_invoice_number == '') {
            $scope.validation_error = "Please enter Supplier invoice number" ;
            return false;
        } else if($scope.purchase.supplier_do_number == ''){
            $scope.validation_error = "Please enter Supplier D.O number";
            return false;
        } else if($scope.purchase.supplier_invoice_date == '') {
            $scope.validation_error = "Please enter Supplier invoice date";
            return false;
        } else if($scope.purchase.purchase_invoice_date == ''){
            $scope.validation_error = "Please enter purchase invoice date";
            return false;
        } else if($scope.purchase.supplier_name == 'select') {
            $scope.validation_error = "Please select supplier";
            return false;
        } else if($scope.payment_mode == '') {
            $scope.validation_error = "Please choose Payment mode";
            return false;
        } else if(!$scope.payment_cheque && $scope.purchase.bank_name == '') {
            $scope.validation_error = "Please enter Bank name";
            return false;
        } else if (!$scope.payment_cheque && $scope.purchase.cheque_no == '') {
            $scope.validation_error = "Please enter Cheque no.";
            return false;
        } else if (!$scope.payment_cheque && $scope.purchase.cheque_date == '') {
            $scope.validation_error = "Please choose Cheque date";
            return false;
        } else if($scope.purchase.purchase_items.length == 0){
            $scope.validation_error = "Please Choose Item";
            return false;
        } else if(!(Number($scope.purchase.purchase_invoice_number) == $scope.purchase.purchase_invoice_number)) {
            
            $scope.validation_error = "Please enter a number as purchase invoice number";
            return false;
        } else if(!(Number($scope.purchase.discount) == $scope.purchase.discount)) {
            $scope.validation_error = "Please enter a number as discount";
        } else if ($scope.purchase.purchase_items.length > 0) {
            for(i=0; i<$scope.purchase.purchase_items.length; i++){
                if ($scope.purchase.purchase_items[i].selling_price == 0 || $scope.purchase.purchase_items[i].selling_price == '') {
                    $scope.validation_error = "Enter selling price for the item with code "+$scope.purchase.purchase_items[i].item_code;
                    return false;
                } else if ($scope.purchase.purchase_items[i].unit_price == 0 || $scope.purchase.purchase_items[i].unit_price == '') {
                    $scope.validation_error = "Enter unit price for the item with code "+$scope.purchase.purchase_items[i].item_code;
                    return false;
                }
            }
        }
        return true;
    }
    $scope.save_purchase = function() {
        if($scope.validate_purchase()) {
            params = { 
                'purchase': angular.toJson($scope.purchase),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/purchase/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/entry/?purchase_type=inventory_based';
               
            }).error(function(data, success){
                
            });
        }
    }

}

function InventoryDNController ($scope, $http, $element, $location) {

    $scope.items = [];
    $scope.customer = 'select';
    $scope.customer_name = '';
    $scope.item_name = '';
    $scope.selected_item = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.delivery_note = {
        'sales_items': [],
        'delivery_note_number': '',
        'customer':'',
        'date': 0,
        'lpo_no': 0,
        'net_total': 0,
        'dn_mode': 'inventory_based',
    }
    $scope.delivery_note.customer = 'select';
    $scope.init = function(csrf_token, delivery_note_number)
    {
        $scope.csrf_token = csrf_token;
        $scope.delivery_note.delivery_note_number = delivery_note_number;
        $scope.popup = '';
        get_customers($scope, $http);
        new Picker.Date($$('#delivery_note_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y', 
        });
    }

    $scope.is_delivery_note_exists = function() {
        check_delivery_note_exists($scope, $http);
    }

    $scope.add_customer = function() {
        $scope.name = '';
        $scope.house = '';
        $scope.street = '';
        $scope.city = '';
        $scope.district = '';
        $scope.pin = '';
        $scope.mobile = '';
        $scope.phone = '';
        $scope.email = '';
        if($scope.customer == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
        
       add_new_customer($http, $scope);
    }
    $scope.get_items = function(parameter) {

        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        if($scope.item_code == '' && $scope.item_name == '') {
            $scope.items = [];
            return false;
        }
        get_inventory_items($scope, $http, parameter, param);
        
    }
    $scope.add_dn_item = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.item_select_error = '';
        if($scope.delivery_note.sales_items.length > 0) {
            for(var i=0; i< $scope.delivery_note.sales_items.length; i++) {
                if($scope.delivery_note.sales_items[i].item_code == item.code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {
            'sl_no': $scope.delivery_note.sales_items.length + 1,
            'item_code': item.code,
            'item_name': item.name,
            'current_stock': item.current_stock,
            'unit_price': item.unit_price,
            'qty_sold': 0,
            'net_amount': 0,
            'type': item.type,
        }
        $scope.delivery_note.sales_items.push(selected_item);
        $scope.item_select_error = '';
    }
    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if (!Number(item.qty_sold) || item.qty_sold == '' || item.qty_sold == undefined) {
            item.qty_sold = 0
        }
        if(item.type == 'item' && parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Quantity for the item with code "+ item.item_code+ " not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            }
        }
        $scope.calculate_net_total_sale();
    }

    $scope.calculate_net_total_sale = function() {
        net_total = 0
        for (var i=0; i < $scope.delivery_note.sales_items.length; i++ ){
            net_total = parseFloat(net_total) + parseFloat($scope.delivery_note.sales_items[i].net_amount);
        }
        $scope.delivery_note.net_total = net_total;
    }

    $scope.remove_from_item_list = function(item) {
        var index = $scope.delivery_note.sales_items.indexOf(item);
        $scope.delivery_note.sales_items.splice(index, 1);
        $scope.calculate_net_total_sale();
    }

    $scope.validate_dn = function() {
        $scope.delivery_note.customer = $scope.customer;
        $scope.delivery_note.date = $$('#delivery_note_date')[0].get('value');
        if($scope.delivery_note.delivery_note_number =='' || $scope.delivery_note.delivery_note_number == undefined){
            $scope.validation_error = "Enter Delivery Note No";
            return false;
        } else if($scope.delivery_note.customer =='' || $scope.delivery_note.customer == undefined || $scope.delivery_note.customer =='select'){
            $scope.validation_error = "choose customer";
            return false;
        } else if($scope.delivery_note.lpo_no =='' || $scope.delivery_note.lpo_no == undefined){
            $scope.validation_error = "enter lpo no";
            return false;
        } else if($scope.delivery_note.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if($scope.delivery_note.sales_items.length > 0){
            for (var i=0; i < $scope.delivery_note.sales_items.length; i++){
                if ($scope.delivery_note.sales_items[i].type == 'item' && parseInt($scope.delivery_note.sales_items[i].current_stock) < parseInt($scope.delivery_note.sales_items[i].qty_sold)){
                    $scope.validation_error = "Quantity not in stock for item with code "+$scope.delivery_note.sales_items[i].item_code;
                    return false;
                }
            }
        } 
        return true;
    }


    $scope.save_delivery_note = function() {

        if($scope.validate_dn()){
            params = { 
                'delivery_note': angular.toJson($scope.delivery_note),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/create_delivery_note/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/delivery_note_pdf/'+data.id+'/';                 
            }).error(function(data, success){
                
            });
        }          
    }

}

function InventorySalesController($scope, $http, $element, $location) {
    $scope.items = [];
    $scope.customer = 'select';
    $scope.customer_name = '';
    $scope.payment_cheque = true;
    $scope.item_name = '';
    $scope.sales = {
        'sales_items': [],
        'sales_invoice_number': '',
        'date_sales': '',
        'customer':'',
        'net_total': 0,
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'bank_name': '',
        'branch': '',
        'cheque_no': '',
        'payment_mode': 'cash',
        'paid': 0,
        'balance': 0,
        'discount': 0,
        'discount_percentage': 0,
        'sales_mode':'inventory_sales',
        'removed_items': [],
        'po_no': '',
        'terms': '',
        'rep': '',
        'via': '',
        'fob': '',
        
    }
    $scope.init = function(csrf_token, invoice_no) {
        $scope.csrf_token = csrf_token;
        $scope.sales.sales_invoice_number = invoice_no;
        $scope.popup = '';
        get_customers($scope, $http);
        new Picker.Date($$('#sales_invoice_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }

    $scope.is_sales_invoice_exists = function() {
        check_sales_invoice_no_exists($scope, $http);
    }

    $scope.get_items = function(parameter) {

        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.item_code;
        else if(parameter == 'item_name')
            var param = $scope.item_name;
        if($scope.item_code == '' && $scope.item_name == '') {
            $scope.items = [];
            return false;
        }
        get_inventory_items($scope, $http, parameter, param);
        
    }
    $scope.add_sales_item = function(item) {
        $scope.selecting_item = false;
        $scope.item_selected = true;
        $scope.item_code = '';
        $scope.item_name = '';
        $scope.item_select_error = '';
        if($scope.sales.sales_items.length > 0) {
            for(var i=0; i< $scope.sales.sales_items.length; i++) {
                if($scope.sales.sales_items[i].item_code == item.code) {
                    $scope.item_select_error = "Item already selected";
                    return false;
                }
            }
        } 
        var selected_item = {
            'sl_no': $scope.sales.sales_items.length + 1,
            'item_code': item.code,
            'item_name': item.name,
            'current_stock': item.current_stock,
            'unit_price': item.unit_price,
            'qty_sold': 0,
            'net_amount': 0,
            'type': item.type,
        }
        $scope.sales.sales_items.push(selected_item);
        $scope.item_select_error = '';
    }
    $scope.calculate_net_total_sale = function() {
        net_total = 0
        for (var i=0; i < $scope.sales.sales_items.length; i++ ){
            net_total = parseFloat(net_total) + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
    }

    $scope.add_customer = function() {
        $scope.name = '';
        $scope.house = '';
        $scope.street = '';
        $scope.city = '';
        $scope.district = '';
        $scope.pin = '';
        $scope.mobile = '';
        $scope.phone = '';
        $scope.email = '';
        if($scope.customer == 'other') {
            $scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#add_customer'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }

    $scope.add_new_customer = function() { 
        
       add_new_customer($http, $scope);
    }
    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if (!Number(item.qty_sold) || item.qty_sold == '' || item.qty_sold == undefined) {
            item.qty_sold = 0
        }
        if(item.type == 'item' && parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Quantity for the item with code "+ item.item_code+ " not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            }
            $scope.calculate_net_total_sale();
        }
    }

    $scope.calculate_discount_percentage = function() {

        if ($scope.sales.discount == '' || !Number($scope.sales.discount)) {
            $scope.sales.discount = 0;
            $scope.sales.discount_percentage = 0;
        }
        if ($scope.sales.net_total == '' || !Number($scope.sales.net_total)) {
            $scope.sales.discount_percentage = 0;
        }
        $scope.sales.discount_percentage = ((parseFloat($scope.sales.discount)/parseFloat($scope.sales.net_total))*100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }
    $scope.calculate_discount_amount = function() {
        if ($scope.sales.discount_percentage == '' || !Number($scope.sales.discount_percentage)) {
            $scope.sales.discount = 0;
            $scope.sales.discount_percentage = 0;
        }
        if ($scope.sales.net_total == '' || !Number($scope.sales.net_total)) {
            $scope.sales.discount = 0;
        }
        $scope.sales.discount = ((parseFloat($scope.sales.discount_percentage) * parseFloat($scope.sales.net_total))/100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }

    $scope.calculate_grant_total_sale = function(){
        if ($scope.sales.net_total == '' || $scope.sales.net_total == undefined || !Number($scope.sales.net_total)){
            $scope.sales.net_total = 0;
        }
        if ($scope.sales.roundoff == '' || $scope.sales.roundoff == undefined || !Number($scope.sales.roundoff)){
            $scope.sales.roundoff = 0;
        }
        if ($scope.sales.discount == '' || $scope.sales.discount == undefined || !Number($scope.sales.discount)){
            $scope.sales.discount = 0;
        }
        $scope.sales.grant_total = (parseFloat($scope.sales.net_total) - (parseFloat($scope.sales.roundoff) + parseFloat($scope.sales.discount))).toFixed(2);
        $scope.calculate_balance_sale();
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = $scope.sales.grant_total - $scope.sales.paid;
    }

    $scope.remove_from_item_list = function(item) {
        var index = $scope.sales.sales_items.indexOf(item);
        $scope.sales.sales_items.splice(index, 1);
        $scope.calculate_net_total_sale();
    }
    $scope.validate_sales = function() {
        $scope.sales.customer = $scope.customer;
        $scope.sales.sales_invoice_date = $$('#sales_invoice_date')[0].get('value');
        $scope.sales.cheque_date = $$('#cheque_date')[0].get('value');
        if($scope.sales.sales_invoice_date == '') {
            $scope.validation_error = "Enter Sales invoice Date" ;
            return false;
        } else if($scope.sales.sales_invoice_number == '' || $scope.sales.sales_invoice_number == undefined) {
            $scope.validation_error = "Enter Invoice no" ;
            return false;
        } else if($scope.sales.customer =='select'){
            $scope.validation_error = "Choose Customer";
            return false;
        } else if($scope.sales.project_id =='select') {
            $scope.validation_error = "Choose Project";
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.bank_name == '' || $scope.sales.bank_name == undefined)){
            $scope.validation_error = "Please enter Bank Name";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.branch == '' || $scope.sales.branch == undefined)){
            $scope.validation_error = "Please enter Branch";
            return false;
        } else if(!($scope.payment_cheque) && ($scope.sales.cheque_no == '' || $scope.sales.cheque_no == undefined)){
            $scope.validation_error = "Please enter Cheque No.";
            return false;
        } else if(!$scope.payment_cheque && ($scope.sales.cheque_date == '' || $scope.sales.cheque_date == undefined)){
            $scope.validation_error = "Please enter Cheque Date.";
            return false;
        } else if ($scope.sales.paid == 0 && $scope.sales.payment_mode == 'cash') {
            $scope.validation_error ="You have choosed cash as payment mode , so please enter the PAID";
            return false;
        } else if ((parseFloat($scope.sales.paid) != parseFloat($scope.sales.grant_total)) && ($scope.sales.payment_mode == 'cash' || $scope.sales.payment_mode == 'cheque')) {
            $scope.validation_error ="Please choose payment mode as credit , because you have balance amount.";
            return false;
        } else if($scope.sales.sales_items.length > 0){
            for (var i=0; i < $scope.sales.sales_items.length; i++){
                if ($scope.sales.sales_items[i].type == 'item' && parseInt($scope.sales.sales_items[i].current_stock) < parseInt($scope.sales.sales_items[i].qty_sold)){
                    $scope.validation_error = "Quantity not in stock for item with code "+$scope.sales.sales_items[i].item_code;
                    return false;
                }
            }
        } 
        return true;
    }
    $scope.save_sales = function() {
        if($scope.validate_sales()) {
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/invoice_pdf/'+data.id+'/';                
            }).error(function(data, success){
                
            });
        }    
    }

}

function EditSalesController($scope, $http, $location, $element) {
    
    $scope.sales = {
        'invoice_no': '',
        'project_name': '',
        'delivery_note_no': '',
        'sales_items': [],
        'removed_items': [],
        'customer': '', 
        'date': '',
        'lpo_number': '',
        'total_amount': '',
        'salesman': '',
        'payment_mode': 'cash',
        'cheque_no': '',
        'bank_name': '',
        'branch': '',
        'cheque_date': '',
        'bank_name': '',
        'net_total': '',
        'net_discount': '',
        'roundoff': 0,
        'grant_total': '',
        'paid': 0,
        'balance': 0,
        'id': '',
        'balance_payment':0,
        'paid_amount': 0,
        'discount_sale': 0,
        'discount_sale_percentage': 0,
        'po_no': '',
        'terms': '',
        'rep': '',
        'via': '',
        'fob': '',
    }

    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.get_sales_invoice_details = function() {
        get_sales_invoice_details($scope, $http, 'sales');
    }
    // $scope.add_invoice = function(invoice) {

    //     $scope.invoice_selected = true;
    //     $scope.sales = invoice;
    //     $scope.invoice_no = invoice.invoice_no;
    //     $scope.payment_mode_change_sales(invoice.payment_mode);
    //     $scope.sales.balance_payment = invoice.balance;
    //     $scope.sales.paid_amount = invoice.paid;
    //     $scope.sales.paid = 0;
    //     $scope.sales.removed_items = [];
    // }

    $scope.calculate_discount_percentage = function() {

        if ($scope.sales.discount_sale == '' || $scope.sales.discount_sale != Number($scope.sales.discount_sale)) {
            $scope.sales.discount_percentage = 0;
        }
        if ($scope.sales.net_total == '' || $scope.sales.net_total != Number($scope.sales.net_total)) {
            $scope.sales.discount_percentage = 0;
        }
        $scope.sales.discount_percentage = ((parseFloat($scope.sales.discount_sale)/parseFloat($scope.sales.net_total))*100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }
    $scope.calculate_discount_amount = function() {
        if ($scope.sales.discount_percentage == '' || $scope.sales.discount_percentage != Number($scope.sales.discount_percentage)) {
            $scope.sales.discount_sale = 0;
        }
        if ($scope.sales.net_total == '' || $scope.sales.net_total != Number($scope.sales.net_total)) {
            $scope.sales.discount_sale = 0;
        }
        $scope.sales.discount_sale = ((parseFloat($scope.sales.discount_percentage) * parseFloat($scope.sales.net_total))/100).toFixed(2);
        $scope.calculate_grant_total_sale();
    }

    $scope.remove_from_item_list = function(item) {
        var index = $scope.sales.sales_items.indexOf(item);
        $scope.sales.removed_items.push(item);
        $scope.sales.sales_items.splice(index, 1);
        
        for (var i=0; i< $scope.sales.sales_items.length; i++) {
            item = $scope.sales.sales_items[i]
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
                $scope.calculate_net_discount_sale();
            }
        }
        $scope.calculate_net_total_sale();
    }

    $scope.calculate_net_total_amount = function() {
        var total_amount = 0
        for(var i=0; i< $scope.sales.sales_items.length; i++){
            total_amount = (parseFloat($scope.sales.sales_items[i].net_amount)).toFixed(2);
        }
        $scope.sales.total_amount = total_amount;
    }

    $scope.calculate_net_amount_sale = function(item) {
        if(parseInt(item.total_qty) < parseInt(item.qty_sold)) {
            $scope.validation_error = "Quantity not in stock";
            return false;
        } else {
            $scope.validation_error = "";
        }
        if(item.qty_sold != '' && item.unit_price != ''){

            var amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);

            item.net_amount = parseFloat(amount);
        }
        $scope.calculate_net_total_sale();
    }

    $scope.calculate_net_amount_sale_qty = function(item) {

        if(item.qty_sold != '' && item.unit_price != ''){
            item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
        }
        $scope.calculate_net_total_sale();
    }
    $scope.calculate_net_total_sale = function(){
        var net_total = 0;
        for(i=0; i<$scope.sales.sales_items.length; i++){
            net_total = net_total + parseFloat($scope.sales.sales_items[i].net_amount);
        }
        $scope.sales.net_total = net_total;
        $scope.calculate_grant_total_sale();
        
    }
    $scope.calculate_grant_total_sale = function(){
        $scope.sales.grant_total = $scope.sales.net_total - $scope.sales.roundoff - $scope.sales.discount_sale;
        $scope.sales.balance = (parseFloat($scope.sales.grant_total) - parseFloat($scope.sales.paid_amount)) - parseFloat($scope.sales.paid);
    }
    $scope.calculate_balance_sale = function () {
        $scope.sales.balance = (parseFloat($scope.sales.grant_total) - parseFloat($scope.sales.paid_amount)) - parseFloat($scope.sales.paid);
    }
    $scope.validate_sales = function() {

        if($scope.sales.invoice_no == '') {
            $scope.validation_error = "Enter Sales Invoice No" ;
            return false;
        } else if($scope.sales.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if ($scope.sales.paid == 0 && $scope.sales.payment_mode == 'cash') {
            $scope.validation_error ="You have choosed cash as payment mode , so please enter the PAID";
            return false;
        } else if (($scope.sales.paid != $scope.sales.grant_total) && ($scope.sales.payment_mode == 'cash' || $scope.sales.payment_mode == 'cheque')) {
            $scope.validation_error ="Please choose payment mode as credit , because you have balance amount.";
            return false;
        } else if($scope.sales.sales_items.length > 0){
            for (var i=0; i < $scope.sales.sales_items.length; i++){
                if ($scope.sales.sales_items[i].unit_price == 0) {
                    $scope.validation_error = "Enter unit price for item "+$scope.sales.sales_items[i].item_name;
                    return false;
                } else if ($scope.sales.sales_items[i].remaining_qty < 0) {
                    $scope.validation_error = "Check the entered Quantity for the item "+$scope.sales.sales_items[i].item_name;
                    return false;
                }
            }
        } 
        return true;       
    }
    $scope.payment_mode_change_sales = function(payment_mode) {
        if(payment_mode == 'cheque') {
            $scope.payment_cheque = false;
            $scope.payment_cheque = false;
            new Picker.Date($$('#cheque_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        } else {
            $scope.payment_cheque = true;
        }
    }
    $scope.edit_sales_invoice = function() {
        if($scope.validate_sales()){
            if ($scope.sales.bank_name == null) {
                $scope.sales.bank_name = '';
            }
            if($scope.sales.payment_mode == null) {
                $scope.sales.payment_mode = 'cash';
            }
            params = { 
                'sales': angular.toJson($scope.sales),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/edit_sales_invoice/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/sales/invoice_pdf/'+data.id+'/';                        
            }).error(function(data, success){
                
            });
        }  
    }
}

function EditDeliveryController($scope, $element, $http, $timeout, share, $location) {

    $scope.items = [];
    $scope.selected_item = '';
    $scope.customer = '';
    $scope.selecting_item = false;
    $scope.item_selected = false;
    $scope.customer_name = '';
    $scope.delivery_note = {
        'id': [],
        'dn_no': '',
        'lpo_no':'',
        'project_name': '',
        'project_id': '',
        'sales_items': '',
        'date': '',
        'customer': '',
        'net_total': 0,
        'is_project': '',
        'removed_items': [],
    }

    $scope.init = function(csrf_token, sales_invoice_number)
    {
        $scope.csrf_token = csrf_token;
    }
    
    $scope.calculate_net_amount_sale = function(item) {
        $scope.validation_error = "";
        if(item.type == 'item' && parseInt(item.qty_sold) > parseInt(item.current_stock)) {
            $scope.validation_error = "Quantity not in stock";
            return false;
        } else {
            if(item.qty_sold != '' && item.unit_price != ''){
                item.net_amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);
            } else {
                item.net_amount = ((parseFloat(item.total_qty)*parseFloat(item.unit_price))).toFixed(2);
            }
            $scope.calculate_net_total_amount();
        }
    }

    $scope.calculate_net_total_amount = function() {
        var total_amount = 0
        for(var i=0; i< $scope.delivery_note.sales_items.length; i++){
            total_amount = (parseFloat(total_amount) + parseFloat($scope.delivery_note.sales_items[i].net_amount)).toFixed(2);
        }
        $scope.delivery_note.net_total = total_amount;
    }

    $scope.get_delivery_note_details = function(){
        get_dn_details($scope, $http, '');
    }

    $scope.delivery_note_validation = function(){
        if ($scope.delivery_note_no == '' || $scope.delivery_note_no == undefined) {
            $scope.validation_error = "Enter delivery note no";
            return false;
        } else if($scope.delivery_note.sales_items.length == 0){
            $scope.validation_error = "Choose Item";
            return false;
        } else if($scope.delivery_note.sales_items.length > 0){
            for (var i=0; i < $scope.delivery_note.sales_items.length; i++){
                if ($scope.delivery_note.sales_items[i].type == 'item' && parseInt($scope.delivery_note.sales_items[i].current_stock) < parseInt($scope.delivery_note.sales_items[i].qty_sold)){
                    $scope.validation_error = "Quantity not in stock for item "+$scope.delivery_note.sales_items[i].item_name;
                    return false;
                } else if ($scope.delivery_note.sales_items[i].unit_price == 0){
                    $scope.validation_error = "Please enter unit price for the item "+$scope.delivery_note.sales_items[i].item_code;
                    return false;
                }
            }
        } 
        return true;
    }
    $scope.remove_from_item_list = function(item) {
        $scope.delivery_note.removed_items.push(item);
        var index = $scope.delivery_note.sales_items.indexOf(item);
        $scope.delivery_note.sales_items.splice(index, 1);
        $scope.calculate_net_total_amount();
    }

    $scope.edit_delivery_note = function() {
        $scope.is_valid = $scope.delivery_note_validation();
        if($scope.is_valid) {
            params = { 
                'delivery_note': angular.toJson($scope.delivery_note),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/sales/edit_delivery_note/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    document.location.href = '/sales/delivery_note_pdf/'+data.id+'/';   

                }
            }).error(function(data, success){
                
            });
        }
    }
}

function AddItemController($scope, $http, $element) {
    $scope.item = {
        'name': '',
        'code': '',
        'type': '',
    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.add_item = function() {
        add_item($scope, $http, 'add_item');
    }
}


function PrintDeliveryNoteController($scope, $http, $element) {
    $scope.delivery_note = {
        'date': '',
        'id': '',
        'dn_no': '',
        'lpo_no': '',
        'project_name': '',
        'sales_items': '',
        'net_total': '',
        'customer': '',

    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.get_delivery_note_details = function() {
        get_dn_details($scope, $http, 'print');
    }
    
    $scope.print_delivery_note = function() {
        document.location.href = '/sales/delivery_note_pdf/'+$scope.dn_id+'/';
    }

}

function PrintInvoiceController($scope, $http, $element) {
    $scope.sales = {
        'date': '',
        'id': '',
        'dn_no': '',
        'lpo_no': '',
        'project_name': '',
        'sales_items': [],
        'net_total': 0,
        'customer': '',
        'invoice_no': '',
        'net_discount': 0,
        'roundoff': 0,
        'grant_total': 0,
        'bank_name': '',
        'branch': '',
        'cheque_no': '',
        'payment_mode': 'cash',
        'paid': 0,
        'balance': 0,
        'discount': 0,
        'discount_percentage': 0,

    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.get_sales_invoice_details = function() {
        get_sales_invoice_details($scope, $http, 'print');
    }
    $scope.print_invoice = function() {
        document.location.href = '/sales/invoice_pdf/'+$scope.sales_id+'/';
    }

}

function CashInHandEntryController($scope, $element, $http) {

    $scope.cash_entry = {
        'from': '',
        'purpose': '',
        'project_id': '',
        'date': '',
        'amount': 0.00,
        'other_purpose': '',
    }
    $scope.is_other_purpose = false;
    $scope.is_project = false;
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_projects($scope, $http);
    }
    $scope.add_purpose = function(){
        var purpose_type = $scope.cash_entry.purpose;
        if (purpose_type == 'project') {
            $scope.is_project = true;
            $scope.is_other_purpose = false;
        } else if (purpose_type == 'other') {
            $scope.is_other_purpose = true;
            $scope.is_project = false;
        } else {
            $scope.is_other_purpose = false;
            $scope.is_project = false;
        }

    }
    $scope.cash_entry_form_validation = function() {
        if ($scope.cash_entry.date == '' || $scope.cash_entry.date == undefined) {
            $scope.validation_error = 'Please enter date';
            return false;
        } else if ($scope.cash_entry.from == '' || $scope.cash_entry.from == undefined) {
            $scope.validation_error = 'Please add from';
            return false;
        } else if ($scope.cash_entry.purpose == '' || $scope.cash_entry.purpose == undefined) {
            $scope.validation_error = 'Please choose purpose';
            return false;
        } else if ($scope.is_project && ($scope.cash_entry.project_id == '' || $scope.cash_entry.project_id == undefined)) {
            $scope.validation_error = 'Please choose project';
            return false;
        } else if ($scope.other_purpose && ($scope.cash_entry.other_purpose == '' || $scope.cash_entry.other_purpose == undefined)) {
            $scope.validation_error = 'Please enter purpose';
            return false;
        } else if ($scope.cash_entry.amount == '' || $scope.cash_entry.amount == undefined) {
            $scope.validation_error = 'Please enter amount';
            return false;
        }
        return true;
    }
    $scope.create_cash_entry = function() {
        $scope.is_valid = $scope.cash_entry_form_validation();
        if($scope.is_valid) {
            params = { 
                'cash_entry': angular.toJson($scope.cash_entry),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/create_cash_entry/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    document.location.href = '/create_cash_entry/';   

                }
            }).error(function(data, success){
                
            });
        }
    }
}

function VendorAccountController($scope, $element, $http, $timeout, $location){  
    $scope.actual_total_amount = 0;
    $scope.actual_amount_paid = 0;
    $scope.actual_balance_amount = 0; 
    $scope.cash = true; 
    $scope.init = function(csrf_token) 
    {
        $scope.csrf_token = csrf_token;
        $scope.vendor_account = {
            'payment_mode': 'cash',
            'total_amount': 0,
            'balance_amount': 0,
            'amount_paid': 0,
            'amount': 0,
            'cheque_no': '',
            'cheque_date': '',
            'bank_name': '',
            'branch_name': '',
            'narration': '',
     }
        $scope.date_picker = new Picker.Date($$('#vendor_account_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
        $scope.date_picker_cheque = new Picker.Date($$('#cheque_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format: '%d/%m/%Y',
        });
        get_suppliers($scope, $http);
    }
    $scope.select_payment_mode = function(){
        if($scope.vendor_account.payment_mode == 'cheque') {
            $scope.cash = false;
        } else {
            $scope.cash = true;
        }
    }
    $scope.get_vendor_account_details = function(){
        var vendor = $scope.vendor_account.vendor;
        $http.get('/purchase/vendor_account/?vendor='+$scope.vendor_account.vendor).success(function(data, status)
        {
            console.log(data.vendor_account);
            if (status==200) {             
                $scope.vendor_account = data.vendor_account;
                $scope.actual_total_amount = data.vendor_account.total_amount;
                $scope.actual_amount_paid = data.vendor_account.amount_paid;
                $scope.actual_balance_amount = data.vendor_account.balance_amount;
                $scope.select_payment_mode();               
            }
            
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate_vendor_account = function(){
        if($scope.vendor_account.vendor == '' || $scope.vendor_account.vendor == undefined ) {
            $scope.validation_error = "Please select Vendor";
            return false;
        } else if($$('#vendor_account_date')[0].get('value') == '') {
            $scope.validation_error = "Please select date";
            return false;
        } else if($scope.vendor_account.amount == '' || $scope.vendor_account.amount == 0 || $scope.vendor_account.amount != Number($scope.vendor_account.amount)){
            $scope.validation_error = "Please enter amount";            
            return false;
        } else if ($scope.vendor_account.balance_amount  < $scope.vendor_account.amount) {
            $scope.validation_error = "Please enter a valid amount";            
            return false;
        }
        if(!$scope.vendor_account.narration){
            $scope.vendor_account.narration = "";
        }
        if($scope.vendor_account.payment_mode == 'cash') {
            if(!$scope.vendor_account.branch_name)
                $scope.vendor_account.branch_name = "";
            if(!$scope.vendor_account.bank_name)
                $scope.vendor_account.bank_name = "";
            if(!$scope.vendor_account.cheque_no)
                $scope.vendor_account.cheque_no = "";
            if(!$scope.vendor_account.cheque_date)
                $scope.vendor_account.cheque_date = "";
        } else {
            if(!$scope.vendor_account.branch_name){
                $scope.validation_error = "Please enter branch name";
                return false;
            } else if(!$scope.vendor_account.bank_name){
                $scope.validation_error = "Please enter bank name";
                return false;
            }else if(!$scope.vendor_account.cheque_no){
                $scope.validation_error = "Please enter cheque no";
                return false;
            }else if($$('#cheque_date')[0].get('value') == ''){
                $scope.validation_error = "Please enter cheque date";
                return false;
            }
            if($$('#cheque_date')[0].get('value') != '') {
                $scope.vendor_account.cheque_date = $$('#cheque_date')[0].get('value');
            }
        }
        return true;
    }
    $scope.reset_vendor_account = function(){
        $scope.vendor_account.vendor = '';
        
    }
    $scope.save_vendor_account = function(){
        $scope.vendor_account.vendor_account_date = $$('#vendor_account_date')[0].get('value');
        
        if($scope.validate_vendor_account()) {
            params = { 
                'vendor_account': angular.toJson($scope.vendor_account),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : '/purchase/vendor_account/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/purchase/vendor_accounts/';
               
            }).error(function(data, success){
                
            });
        }
          
    }
}
function AddOpeningStockController($scope, $http, $element) {
    $scope.openingstock = {
        'item_code':'',
        'quantity': '',
        'unit_price': '',
        'selling_price': '',
    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.opening_stock_validation = function() {
        if ($scope.openingstock.quantity == '' || $scope.openingstock.quantity == undefined || (! Number($scope.openingstock.quantity))) {
            $scope.validation_error = 'Please enter the quantity';
            return false;
        } else if ($scope.openingstock.unit_price == '' || $scope.openingstock.unit_price == undefined || (! Number($scope.openingstock.unit_price))) {
            $scope.validation_error = 'Please enter the unit price';
            return false;
        } else if ($scope.openingstock.selling_price == '' || $scope.openingstock.selling_price == undefined || (! Number($scope.openingstock.selling_price))) {
            $scope.validation_error = 'Please enter the selling price';
            return false;
        }
        return true;
    }

    $scope.save_opening_stock = function(){
        $scope.is_valid = $scope.opening_stock_validation();
        if ($scope.is_valid){
            params = { 
                'opening_stock_details': angular.toJson($scope.openingstock),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/project/add_stock/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                console.log()
            }).error(function(data, success){
                console.log()
            
        });

        }

    }
    $scope.get_items = function(parameter) {

        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.openingstock.item_code;
        
        if($scope.openingstock.item_code == '' && $scope.openingstock.item_name == '') {
            $scope.items = [];
            return false;
        }
        get_inventory_items($scope, $http, parameter, param);
        
    }


}