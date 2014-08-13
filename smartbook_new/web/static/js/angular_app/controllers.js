/************* Common JS Methods ****************************/
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function get_inventory_items($scope, $http, parameter, param){
    $http.get('/inventory/items/?inventory_item=true&'+parameter+'='+param).success(function(data)
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

function item_validation($scope) {
    if ($scope.item.name == '' || $scope.item.name == undefined) {
        $scope.validation_error = 'Please ente the Name';
        return false;
    } else if ($scope.item.code == '' || $scope.item.code == undefined) {
        $scope.validation_error = 'Please enter the Code';
        return false;
    } 
    return true;
}

function add_item($scope, $http, from) {
    $scope.is_valid = item_validation($scope);
    if ($scope.is_valid) {
        params = { 
            'item_details': angular.toJson($scope.item),
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        $http({
            method : 'post',
            url : "/inventory/add_item/",
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
                }
            }
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
            } else {
                if (from == 'add_item') {
                    document.location.href = '/inventory/items/';
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
function get_suppliers($scope, $http) {
    $http.get('/suppliers/').success(function(data)
    {
        $scope.suppliers = data.suppliers;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function validate_add_supplier($scope) {
    $scope.validation_error = '';
    console.log($scope.email);
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
    } else if (($scope.email != undefined) && !(validateEmail($scope.email))) {
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
            url : "/create_supplier/",
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
                $scope.name = '';
                $scope.contact_person = '';
                $scope.house_name = '';
                $scope.street = '';
                $scope.city = '';
                $scope.district = '';
                $scope.pin = '';
                $scope.mobile = '';
                $scope.phone = '';
                $scope.email = '';
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
    $http.get('/customers/').success(function(data)
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
    } else if($scope.email_id != undefined && !validateEmail($scope.email_id)) {
        $scope.error_message = "Please enter a valid email id";
        $scope.error_flag = true;
        return false;
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
            $scope.error_flag=true;
            $scope.message = data.message;
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
function get_sales_invoice_details($scope, $http, from) {
    $scope.invoice_message = '';
        
    var invoice_no = $scope.invoice_no;
    

    $http.get('/sales/invoice_details/?invoice_no='+invoice_no).success(function(data)
    {
        if (from == 'sales') {
            $scope.sales = {
                'invoice_no': '',
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
                console.log($scope.sales.sales_items)
                $scope.payment_mode_change_sales($scope.sales.payment_mode);
                $scope.sales.balance_payment = $scope.sales.balance;
                $scope.sales.paid_amount = $scope.sales.paid;
                $scope.sales.paid = 0;
                $scope.sales.removed_items = [];
                for (var i=0; i<$scope.sales.sales_items.length; i++){
                    $scope.sales.sales_items[i].sold_qty = $scope.sales.sales_items[i].qty_sold
                }
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
/****************** End Common JS Methods ****************************/

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
        'branch': '',
        'bank_name': '',
        'amount': 0,
    }
    $scope.expense_heads = [];
    $scope.expense_head = '';
    $scope.payment_mode_selection = true;
    $scope.is_valid = false;
    $scope.error_flag = false;
    $scope.error_message = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        get_expense_head_list($scope, $http);
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
        } 
    }
    $scope.get_report_type = function(){
        if ($scope.report_type == 'date_based') {
            $scope.date_based = true;
        } 
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
        } else if($scope.purchase.supplier_name == 'select' || $scope.purchase.supplier_name == 'other') {
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
                } else if ($scope.purchase.purchase_items[i].qty_purchased == 0 || $scope.purchase.purchase_items[i].qty_purchased == '') {
                    $scope.validation_error = "Enter quantity for the item with code "+$scope.purchase.purchase_items[i].item_code;
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
                console.log(status)
                document.location.href = '/purchase/entry/?purchase_type=inventory_based';
               
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
        'status': 'estimate',
        
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
        $scope.customer_name = '';
        $scope.house = '';
        $scope.street = '';
        $scope.city = '';
        $scope.district = '';
        $scope.pin = '';
        $scope.mobile = '';
        $scope.land_line = '';
        $scope.email_id = '';
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
    $scope.payment_mode_change_sales = function(type) {
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
        } else if($scope.sales.status == '' || $scope.sales.status == undefined) {
            $scope.validation_error = "Choose Type";
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
        } else if ((parseFloat($scope.sales.paid) != parseFloat($scope.sales.grant_total))&&($scope.sales.balance !=0) && ($scope.sales.payment_mode == 'cash' || $scope.sales.payment_mode == 'cheque')) {
            $scope.validation_error ="Please choose payment mode as credit , because you have balance amount.";
            return false;
        } else if($scope.sales.sales_items.length > 0){
            for (var i=0; i < $scope.sales.sales_items.length; i++){
                if (parseInt($scope.sales.sales_items[i].current_stock) < parseInt($scope.sales.sales_items[i].qty_sold)){
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
        var newly_purchased = parseInt(item.qty_sold) - parseInt(item.sold_qty);
        if(parseInt(item.current_stock) < parseInt(newly_purchased)) {
            $scope.validation_error = "Quantity not in stock for item "+item.item_name;
            return false;
        } else {
            $scope.validation_error = "";
            if(item.qty_sold != '' && item.unit_price != ''){

                var amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);

                item.net_amount = parseFloat(amount);
            }
            $scope.calculate_net_total_sale();
        }
    }

    $scope.calculate_net_amount_sale_qty = function(item) {
        var newly_purchased = parseInt(item.qty_sold) - parseInt(item.sold_qty);
        if(parseInt(item.current_stock) < parseInt(newly_purchased)) {
            $scope.validation_error = "Quantity not in stock for item "+item.item_name;
            return false;
        } else {
            $scope.validation_error = "";
            if(item.qty_sold != '' && item.unit_price != ''){

                var amount = ((parseFloat(item.qty_sold)*parseFloat(item.unit_price))).toFixed(2);

                item.net_amount = parseFloat(amount);
            }
            $scope.calculate_net_total_sale();
        }
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
        } else if ($scope.sales.balance < 0) {
            $scope.validation_error ="Please check Paid amount entered";
            return false;
        } else if($scope.sales.sales_items.length > 0){
            for (var i=0; i < $scope.sales.sales_items.length; i++){
                var newly_purchased = parseInt($scope.sales.sales_items[i].qty_sold) - parseInt($scope.sales.sales_items[i].sold_qty);
                if ($scope.sales.sales_items[i].unit_price == 0) {
                    $scope.validation_error = "Enter unit price for item "+$scope.sales.sales_items[i].item_name;
                    return false;
                } else if (parseInt($scope.sales.sales_items[i].current_stock) < parseInt(newly_purchased)) {
                    $scope.validation_error = "Quantity not in stock for item with code "+$scope.sales.sales_items[i].item_code;
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
function AddItemController($scope, $http, $element) {
    $scope.item = {
        'name': '',
        'code': '',
    }
    $scope.init = function(csrf_token, item_id) {
        $scope.csrf_token = csrf_token;
        $scope.item_id = item_id;
        if(item_id > 0) {
            $http.get('/inventory/edit_item/'+item_id+'/').success(function(data){
                $scope.item = data.item[0];
            }).error(function(data, status){
                console.log('Request failed' || data);
            })
        }
    }
    $scope.add_new_item = function() {
        add_item($scope, $http, 'add_item');
    }
    $scope.edit_item = function() {
        if (item_validation($scope)) {
            params = { 
                'item': angular.toJson($scope.item),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            $http({
                method : 'post',
                url : "/inventory/edit_item/"+$scope.item_id+'/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href = '/inventory/items/';                        
            }).error(function(data, success){
                
            });
        }
    }
}
function PrintInvoiceController($scope, $http, $element) {
    $scope.sales = {
        'date': '',
        'id': '',
        'dn_no': '',
        'lpo_no': '',
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
        console.log($scope.sales_id)
        if($scope.sales_id == '' || $scope.sales_id == undefined){
            $scope.invoice_message = "Please enter a invoice number";
            
        }else{
            
            document.location.href = '/sales/invoice_pdf/'+$scope.sales_id+'/';
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
        
            
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
                console.log(data.message)
            } else {            
                $scope.vendor_account = data.vendor_account;
                $scope.actual_total_amount = data.vendor_account.total_amount;
                $scope.actual_amount_paid = data.vendor_account.amount_paid;
                $scope.actual_balance_amount = data.vendor_account.balance_amount;
                $scope.select_payment_mode();               
            }
            
        }).error(function(data, status)
        {
            // $scope.error_flag=true;
            // $scope.message = data.message;
            
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
            console.log($scope.vendor_account)
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
function VendorAccountReportController($scope, $element, $http, $location) {
      
    $scope.report_date_wise_flag = true;
    $scope.report_vendor_wise_flag = false;
    
    $scope.init = function(csrf_token,report_type) {
        $scope.report_type = report_type;
        $scope.csrf_token = csrf_token;
        $scope.get_report_type();
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
        
        $scope.get_vendors();

    }
    $scope.get_vendors = function() {
        $http.get('/suppliers/').success(function(data)
        {   
            $scope.suppliers = data.suppliers;
            console.log($scope.suppliers)
            $scope.supplier_name = 'select';
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }

    $scope.get_report_type = function(){
        if($scope.report_type == 'date') {
            $scope.report_date_wise_flag = true;
            $scope.report_vendor_wise_flag = false;
        } else if ($scope.report_type == 'vendor') {
            $scope.report_date_wise_flag = false;
            $scope.report_vendor_wise_flag = true;
        }
    }
    
}
function VendorReportController($http, $scope, $location, $element) {

    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.get_vendors()
    }
    $scope.get_vendors = function() {
        $http.get('/suppliers/').success(function(data)
        {
            $scope.suppliers = data.suppliers[0];
            console.log($scope.suppliers)
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        $scope.supplier_name = 'select';
    }

}
function StockEditController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, item_code) {
        $scope.scrf_token = csrf_token;
        $http.get('/inventory/edit_stock/?openingstock_item_code='+openingstock_item_code).success(function(data)
        {
            $scope.stock = data.stock;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate = function() {
        $scope.validation_error = '';
        if( $scope.stock.quantity != Number($scope.stock.quantity)){
            $scope.validation_error = "Please enter digits as quantity ";
            return false;
        } else if( $scope.stock.unit_price != Number($scope.stock.unit_price)){
            $scope.validation_error = "Please enter digits as unit price ";
            return false;
        } else if( $scope.stock.selling_price != Number($scope.stock.selling_price)){
            $scope.validation_error = "Please enter digits as selling price ";
            return false;
        }else if( $scope.stock.discount_permit_amount != '' && $scope.stock.discount_permit_amount != Number($scope.stock.discount_permit_amount)){
            $scope.validation_error = "Please enter digits as discount amount ";
            return false;
        }else if( $scope.stock.discount_permit_percent != '' && $scope.stock.discount_permit_percent != Number($scope.stock.discount_permit_percent)){
            $scope.validation_error = "Please enter digits as discount percent ";
            return false;
        } else {
            document.getElementById("edit_stock_form").submit();
            return true;
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
        if($scope.openingstock.item_code == ''|| $scope.openingstock.item_code == undefined){
            $scope.validation_error ='Please enter item code';
            return false;
        }else if ($scope.openingstock.quantity == '' || $scope.openingstock.quantity == undefined || (! Number($scope.openingstock.quantity))) {
            $scope.validation_error = 'Please enter the quantity';
            return false;
        } else if ($scope.openingstock.unit_price == '' || $scope.openingstock.unit_price == undefined || (! Number($scope.openingstock.unit_price))) {
            $scope.validation_error = 'Please enter the unit price';
            return false;
        } else if ($scope.openingstock.selling_price == '' || $scope.openingstock.selling_price == undefined || (! Number($scope.openingstock.selling_price))) {
            $scope.validation_error = 'Please enter the selling price';
            return false;
        } return true;
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
                url : "/inventory/add_stock/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                document.location.href = '/inventory/stocks/';
            }).error(function(data, success){
                console.log('error', data);
            });
        }
    }
    $scope.get_items = function(parameter) {
        $scope.validation_error = '';
        if(parameter == 'item_code')
            var param = $scope.item_code;
        if($scope.item_code == '' ) {
            $scope.items = [];
            return false;
        }
        get_inventory_items($scope, $http, parameter, param); 
    }
    $scope.add_item = function(item){
        $scope.item_selected = true;
        $scope.item_code = item.code;
        $scope.openingstock.item_code = item.code;
    }
}