/**
 * Created by Calum on 15/03/2015.
 */

var portfolio_worth =0;
var symbol;
var recent_close;
var recent_date;
var quantity;
var shares_owned;
var cash;
var userList={};

//Initise tooltips
 $(function () {
                  $('[data-toggle="tooltip"]').tooltip()
                });

//Table sorting/searching

$("th.sort").click(function(event){
    $("th.sort").children("span").removeClass("glyphicon glyphicon-triangle-top glyphicon-triangle-bottom");
    $("th.sort.asc").children("span").addClass("glyphicon glyphicon-triangle-top");
    $("th.sort.desc").children("span").addClass("glyphicon glyphicon-triangle-bottom");
});

//Deposit Cash ajax
$(document).ready(function() {
    $('#depositForm').submit( function(event){
        event.preventDefault();
        var amount = $("#deposit_amount").val();
            $.ajax({
                url: "/deposit_cash/",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrf,
                    amount: amount,
                    ni: ni
                },
                success: function (json){
                    if(json["result"] == "success"){
                        bootbox.alert("Cash deposited");
                        cash= json["new_amount"];
                        $(".client_cash_available").html(cash);
                        $("#DepositModal").modal("toggle");
                    }else if(json["result"] == "Insufficient funds"){
                        bootbox.alert('Insufficient funds');

                    }else if(json["result"] == "Client not found"){
                        bootbox.alert("Client not found")
                    }else if(json["result"]=="amount_error"){
                        bootbox.alert("Please enter an amount")
                    }else{
                        bootbox.alert('Error, please seek the system administrator')
                    }
                },
                error: function (xhr, errmsg, err) {
                    bootbox.alert('Failed.');
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
    })
    });

//Withdraw Cash ajax call
$(document).ready(function() {
    $('#withdrawForm').submit( function(event){
        event.preventDefault();
        var amount = $("#withdraw_amount").val();
            $.ajax({
                url: "/withdraw_cash/",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrf,
                    amount: amount,
                    ni: ni
                },
                success: function (json){
                    if(json["result"] == "success"){
                        bootbox.alert("Cash withdrawn");
                        cash= json["new_amount"];
                        $(".client_cash_available").html(parseInt(cash).toFixed(2));
                        $("#WithdrawModal").modal("toggle");
                    }else if(json["result"] == "Insufficient funds"){
                        bootbox.alert('Insufficient funds');

                    }else if(json["result"] == "Client not found") {
                        bootbox.alert("client not found")

                    }else if(json["result"]=="amount_error"){
                        bootbox.alert("Please enter an amount")
                    }else{
                        bootbox.alert('Error, please seek the system administrator')
                    }
                },
                error: function (xhr, errmsg, err) {
                    bootbox.alert('Failed.');
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
    })
});

// Buy Stock ajax call
$(document).ready(function(){
    $("#buy_buttonForm").submit(function (event){
        event.preventDefault();
        quantity = $("#buy_quantity").val();
        if (quantity == ""){
            quantity = 1;
        }
        var data = {
                    csrfmiddlewaretoken: csrf,
                    symbol: symbol,
                    ni: ni,
                    price: recent_close,
                    amount: quantity,
                    date: recent_date,
                    buy: 'True'
                };
        $.ajax({
                url: "/buy_stock/",
                type: "POST",
                data: data,
                success: function (json){
                    if(json["result"] == "success"){
                        bootbox.alert("Stocks bought");
                        append_stock_table(data);
                        portfolio_worth += (recent_close * quantity);
                        var sym = data["symbol"].replace(".","");
                        var count = parseInt(parseInt($("#"+sym+"td").html())+data["amount"]);
                        $("#"+sym+"td").html(count);
                        if (count >0){
                            $("button[data-symbol='"+data['symbol']+"']").removeAttr("disabled")
                        }
                        $(".portfolio_worth").html(portfolio_worth.toFixed(2));
                        var total = ($("#"+symbol+"total").html).replace("$","");
                        total = parseInt(total)+(recent_close * quantity);
                        $("#"+symbol+"total").html("$"+total);
                        $("#StockModal").modal("toggle");
                    }else if(json["result"] == "Insufficient funds"){
                        bootbox.alert('Insufficient funds');
                    }else{
                        bootbox.alert('Error, please seek the system administrator')
                    }
                },
                error: function (xhr, errmsg, err) {
                    bootbox.alert('Failed.');
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
    })
});

// Sell Stock ajax call
$(document).ready(function(){
$("#sell_buttonForm").submit(function (event){
    event.preventDefault();
    quantity = $("#sell_quantity").val();
    if (quantity == ""){
        quantity = 1;
    }
    var data = {
                csrfmiddlewaretoken: csrf,
                symbol: symbol,
                ni: ni,
                price: recent_close,
                amount: quantity,
                date: recent_date,
                buy: 'False'
            };
    $.ajax({
            url: "/sell_stock/",
            type: "POST",
            data: data,
            success: function (json) {
                if (json["result"] == "success") {
                    bootbox.alert("Stocks Sold");
                    append_stock_table(data);
                    cash= json["new_amount"];
                    $(".client_cash_available").html(cash);
                    portfolio_worth -= (recent_close * quantity);
                    $(".portfolio_worth").html(portfolio_worth.toFixed(2));
                    var sym = data["symbol"].replace(".","");
                    var count = parseInt($("#"+sym+"td").html())-data["amount"];
                    $("#"+sym+"td").html(count);
                    if (count ==0){
                        $("button[data-symbol='"+data['symbol']+"']").attr("disabled","disabled")
                    }
                    $("#SellStockModal").modal("toggle");
                } else if (json["result"] == "Insufficient funds") {
                    bootbox.alert('Insufficient funds');
                }else if(json["result"] == "No such stock"){
                    bootbox.alert("Error, that stock doesn't exist");
                }else if (json["result"] == "Not enough stock owned"){
                    bootbox.alert('Not enough stock owned to sell desired amount.');
                }else{
                    bootbox.alert('Error, please seek the system administrator')
                }
            },
            error: function (xhr, errmsg, err) {
                bootbox.alert('Failed.');
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    })
});

//Look up buy stock
$(document).ready(function() {
        $('#buySharesForm').submit( function(event){
            event.preventDefault();
            $("#search_stock_submit").button('loading');
            var symbol = $("#stock_symbol").val();
                $.ajax({
                    url: "/query_api/",
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrf,
                        symbol: symbol,
                        days: 5,
                        ni: ni
                    },
                    success: function (json){
                        $("#search_stock_submit").button('reset');
                        if (json.result == "Stock not found"){
                            $("#stock_not_found").removeClass("hidden");
                            $("#stock_graph").addClass("hidden");
                            $("#lineLegend").addClass("hidden");
                            $("#modal_footer").addClass("hidden");
                            $("#stock_buy").addClass("hidden");
                            $("#symbol_title").addClass("hidden");
                        }else if (json.result == "success"){
                            print_results(json);
                        }else{
                             bootbox.alert('Error, please seek the system administrator')
                        }
                    },
                    error: function (xhr, errmsg, err) {
                        $("#search_stock_submit").button('reset');
                        bootbox.alert('Failed.');
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
        })
    });

//Print buy stock results
function print_results(json) {
        var result = json.query.results.quote;
        symbol = result[0]["Symbol"].toUpperCase();
        recent_close = result[0]["Adj_Close"];
        recent_date = result[0]["Date"];
        shares_owned = json["shares_owned"]
        $("#symbol_title").html(symbol);

        $("#stock_not_found").addClass("hidden");

        $("#symbol_title").removeClass("hidden");
        $("#table_div").removeClass("hidden");
        $("#buy_stock_graph").removeClass("hidden");
        $("#lineLegend").removeClass("hidden");
        $("#modal_footer").removeClass("hidden");
        $("#stock_buy").removeClass("hidden");

        make_graph(result,"buy_stock_graph","buy_lineLegend");
        setup_buysell_text()
    }

//Look up sell stock
$(document).ready(function() {
        $('#sellSharesForm').submit( function(event){
            event.preventDefault();
            $("#sell_search_stock_submit").button('loading');
            $("#sell_search_stock_submit").removeClass("hidden");
            var symbol = $("#sell_stock_symbol").val();

                $.ajax({
                    url: "/query_api/",
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrf,
                        symbol: symbol,
                        ni: ni,
                        price: recent_close
                    },
                    success: function (json) {
                        $("#sell_search_stock_submit").button('reset');
                        $("#sell_search_stock_submit").addClass('hidden');

                        if (json["result"] == "Stock not found") {
                            $("#sell_stock_not_found").removeClass("hidden");
                            $("#sell_stock_graph").addClass("hidden");
                            $("#sell_lineLegend").addClass("hidden");
                            $("#sell_modal_footer").addClass("hidden");
                            $("#stock_sell").addClass("hidden");
                            $("#sell_symbol_title").addClass("hidden");

                        }else if(json["result"] == "success"){
                            print_sell_results(json);
                        }
                    },
                    error: function (xhr, errmsg, err) {
                        $("#search_stock_submit").button('reset');
                        bootbox.alert('Failed.');
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
        })
    });

//Print sell stock results
function print_sell_results(json) {
         var result = json.query.results.quote;
         symbol = result[0]["Symbol"].toUpperCase();
         recent_close = result[0]["Adj_Close"];
         recent_date = result[0]["Date"];
         shares_owned = json["shares_owned"]
         $("#sell_symbol_title").html(symbol);
         $("#sell_stock_not_found").addClass("hidden");
         $("#sell_symbol_title").removeClass("hidden");
         $("#table_div").removeClass("hidden");
         $("#sell_stock_graph").removeClass("hidden");
         $("#sell_lineLegend").removeClass("hidden");
         $("#sell_modal_footer").removeClass("hidden");
         $("#stock_sell").removeClass("hidden");
         make_graph(result,"sell_stock_graph","sell_lineLegend");
     }

//Create stock graph
function make_graph(result, graph_str, legend_str) {
        var dates = [];
        var open = [];
        var close = [];
        var high = [];
        var low = [];

        for (var key in result){
            dates[dates.length] = result[key]["Date"];
            open[open.length] = result[key]["Open"] ;
            close[close.length] = result[key]["Close"] ;
            high[high.length] = result[key]["High"] ;
            low[low.length] = result[key]["Low"] ;
        }

        var stock_graph = document.getElementById(graph_str).getContext('2d');
        var stockData = {
            labels: dates,
            datasets: [
                {
                    label: "Open",
                    fillColor: "rgba(223,181,17,0)",
                    strokeColor: "#DFB511",
                    pointColor: "#DFB511",
                    pointStrokeColor: "#34495e",
                    data: open
                },
                {
                    label: "Close",
                    fillColor: "rgba(0,107,195,0)",
                    strokeColor: "#006BC3",
                    pointColor: "#006BC3",
                    pointStrokeColor: "#34495e",
                    data: close
                },
                {
                    label: "High",
                    fillColor: "rgba(9,192,9,0)",
                    strokeColor: "#09C009",
                    pointColor: "#09C009",
                    pointStrokeColor: "#34495e",
                    data: high
                },
                {
                    label: "Low",
                    fillColor: "rgba(218,7,7,0)",
                    strokeColor: "#DA0707",
                    pointColor: "#DA0707",
                    pointStrokeColor: "#34495e",
                    data: low
                }

            ]
        };
        var opts = {scaleFontColor: "#000000",
            scaleLineColor: "#000000",
            scaleGridLineColor: "#000000",
            scaleShowLabels: true,
            bezierCurve: false,
            scaleShowVerticalLines: true,
            responsive: true
        };

        new Chart(stock_graph).Line(stockData, opts);
        legend(document.getElementById(legend_str), stockData);
    }

//Setup text for buy sell footer
function setup_buysell_text(){
        $(".buysell_text").html(" "+symbol+" shares owned: "+shares_owned+"<br>1 "+symbol+" share at $"+ recent_close);
    }

//append shares table
function append_stock_table(data){
        var d = moment(data['date']);
        var purchase;
        if(data["buy"]=='True'){
            purchase="<span class='glyphicon glyphicon-chevron-up'></span>Bought";
        }else{
            purchase="<span class='glyphicon glyphicon-chevron-down'></span>Sold";
        }
        var stock_a = "<a href='/?symbol="+data['symbol']+"'>"+data['symbol']+"</a>";
        var stock_sell = "<button class='btn btn-default btn-xs' data-toggle='modal' data-target='#SellStockModal' data-symbol="+data["symbol"]+">Sell</button>";
        data['symbol'] = data['symbol'].replace(".","");
        if (userList[data['symbol']]== undefined) {
            var t = (data['price'] * data["amount"]);
            var s = '<tr >' +
                '<td class="sort"  data-toggle="collapse" data-target="#' + data['symbol'] + 'div" class="accordion-toggle"><a href="/?symbol='+data['symbol']+'">' + data['symbol'] + '</td>' +
                '<td class="accordion-toggle" data-toggle="collapse" data-target="#'+data["symbol"]+'div" >'+data["amount"]+'</td>' +
                '<script>'+
                '$("td[data-target=\'#'+data["symbol"]+'div\']").attr("data-target", "#'+data["symbol"]+'")'+
                '</script>'+
                '<td ><button class="btn btn-default btn-xs" data-toggle="modal" data-target="#SellStockModal" data-symbol="'+data["symbol"]+'">Sell</button> </td>'+
                '</tr>' +
                '<tr class="hiddenRow">' +
                '<td colspan="3" class="hiddenRow" >' +
                '<div class="accordian-body collapse" id="'+data["symbol"]+'">' +
                '<table class="table table-condensed table-bordered" style="margin-bottom: 0px">' +
                '<thead>' +
                '<th class="sort" data-sort="buy">Purchase <span ></span></th>' +
                '<th class="sort" data-sort="stock" id="stock_th">Stock <span></span></th>' +
                '<th class="sort" data-sort="date">Date<span class="glyphicon glyphicon-triangle-top"></span></th>' +
                '<th class="sort" data-sort="amount">Amount <span></span></th>' +
                '<th class="sort" data-sort="price">Price($) <span></span></th>' +
                '<th class="sort" data-sort="total">Total($) <span></span></th>' +
                '</thead>' +
                '<tbody class="list">' +
                   '<tr>'+
                        '<td class="buy '+data["symbol"]+'">'+purchase+

                        '</td>'+
                        '<td class="stock"><a href="/?symbol='+data["symbol"]+'">'+data["symbol"]+'</a></td>'+
                        '<td class="date">'+d.format("YYYY-MM-DD")+'</td>'+
                        '<td class="amount">'+data["amount"]+'</td>'+
                        '<td class="price">'+data["price"]+'</td>'+
                        '<script>'+
                           'portfolio_worth = (portfolio_worth + parseFloat('+t+'));'+
                        '</script>'+
                        '<td class="total">'+t+'</td>'+
                    '</tr>'+
                '</tbody>' +
                '</table>' +
                '<script>' +
                '$(".portfolio_worth").html(portfolio_worth.toFixed(2));' +
                //Table sorting and searching setup
                'var options ={valueNames: ["buy", "stock", "date", "amount", "price", "total"]};' +
                'userList["' + data["symbol"] + '"] = new List("'+data["symbol"]+'",options);' +
                'userList["' + data["symbol"] + '"].sort("date", { order: "asc"});' +
                '$("th.sort").click(function(event){' +
                '$("th.sort").children("span").removeClass("glyphicon glyphicon-triangle-top glyphicon-triangle-bottom");' +
                '$("th.sort.asc").children("span").addClass("glyphicon glyphicon-triangle-top");' +
                '$("th.sort.desc").children("span").addClass("glyphicon glyphicon-triangle-bottom");' +
                ' });' +
                '</script></div></td></tr>';

            $("#clients_stock_tbody").append(s);
            sell_button_listener();
        }else {
            if (data['buy'] == 'True') {
                var s = "<span class='glyphicon glyphicon-chevron-up'></span>Bought"
            } else {
                var s = "<span class='glyphicon glyphicon-chevron-down'></span>Sold"
            }
            userList[data['symbol']].add({buy: s, stock: stock_a, date: d.format("YYYY-MM-DD"), amount: data['amount'], price: data['price'], total: (data['price'] * data['amount']).toFixed(2)});
            //userList[data['symbol']].sort("stock", { order: "asc"});
            sell_button_listener();
        }
}

function sell_button_listener(){
    $("button[data-target='#SellStockModal']").one('click',function(event){
        var sell_symbol =$(this).attr("data-symbol");
        $("#sell_stock_symbol").val(sell_symbol);
        $("#sellSharesForm").submit();
    });

}