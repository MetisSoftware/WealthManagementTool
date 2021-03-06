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
                        var sym = data["symbol"].replace(".","").toUpperCase();
                        var count = parseInt(parseInt($("#"+sym+"td").html())+data["amount"]);
                        $("#"+sym+"td").html(count);

                        if (count >0){
                            $("button[data-symbol='"+sym+"']").removeAttr("disabled")
                        }
                        portfolio_worth = parseFloat(portfolio_worth);
                        cash = parseFloat(json["new_amount"]);
                        $(".client_cash_available").html(cash.toFixed(2));
                        $(".portfolio_worth").html(portfolio_worth.toFixed(2));
                        $("#"+sym+"td").html(json["stock_amount"]);
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
                    cash= parseFloat(json["new_amount"]).toFixed(2);
                    $(".client_cash_available").html(cash);
                    portfolio_worth -= (recent_close * quantity);
                    $(".portfolio_worth").html(portfolio_worth.toFixed(2));
                    var sym = data["symbol"].replace(".","").toUpperCase();
                    var count = parseInt(json["stock_amount"])-data["amount"];

                    $("#"+sym+"td").html(count);
                    if (count <=0){
                        $("button[data-symbol='"+data['symbol']+"']").attr("disabled","disabled")
                    }
                    portfolio_worth = parseFloat(portfolio_worth);
                    $("#"+sym+"td").html(count);
                    $(".portfolio_worth").html(portfolio_worth.toFixed(2));
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
            do_buy_lookup(7);
        });
        $("#buy_graph_timescale").submit(function(event){
            event.preventDefault();
            $("#buy_graph_timescale > div > button.active").removeClass("active");
            $(this).find("button[type=submit]:focus").addClass("active");
            do_buy_lookup($(this).find("button[type=submit]:focus").attr("value"));

        })
    });

function do_buy_lookup(num){
    $("#search_stock_submit").button('loading');
            days = parseInt(num);
            var symbol = $("#stock_symbol").val();
            $("#buy_stock_graph").addClass('hidden');
            $("#buy_stock_graph_loading").removeClass('hidden');
                $.ajax({
                    url: "/query_api/",
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrf,
                        symbol: symbol,
                        days: days,
                        ni: ni
                    },
                    success: function (json){
                        $("#buy_stock_graph_loading").addClass('hidden');
                        $("#search_stock_submit").button('reset');
                        if (json.result == "Stock not found"){
                            $("#stock_not_found").removeClass("hidden");
                            $("#stock_graph").addClass("hidden");
                            $("#lineLegend").addClass("hidden");
                            $("#modal_footer").addClass("hidden");
                            $("#stock_buy").addClass("hidden");
                            $("#symbol_title").addClass("hidden");
                            $("#buy_graph_timescale").addClass("hidden")
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
}

//Print buy stock results
function print_results(json) {
        var result = json.query.results.quote.reverse();
        symbol = result[result.length-1]["Symbol"].toUpperCase();
        recent_close = result[result.length-1]["Adj_Close"];
        recent_date = result[result.length-1]["Date"];
        shares_owned = json["shares_owned"];
        $("#symbol_title").html(symbol);

        $("#stock_not_found").addClass("hidden");
        $("#buy_graph_timescale").removeClass("hidden");
        $("#symbol_input").attr("value",symbol);
        $("#symbol_title").removeClass("hidden");
        $("#table_div").removeClass("hidden");
        $("#buy_stock_graph").removeClass("hidden");
        $("#buy_lineLegend").removeClass("hidden");
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
            do_sell_lookup(7);

        });
        $("#sell_graph_timescale").submit(function(event){
            event.preventDefault();
            $("#sell_graph_timescale > div > button.active").removeClass("active");
            $(this).find("button[type=submit]:focus").addClass("active");
            do_sell_lookup($(this).find("button[type=submit]:focus").attr("value"));

        })
    });

function do_sell_lookup(d){
                var days = parseInt(d);
                var sym = $("#sell_stock_symbol").val();
                $("#sell_stock_graph").addClass('hidden');
                $("#sell_stock_graph_loading").removeClass('hidden');
                $.ajax({
                    url: "/query_api/",
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrf,
                        symbol: sym,
                        ni: ni,
                        days: days
                    },
                    success: function (json) {
                        $("#sell_search_stock_submit").button('reset');
                        $("#sell_search_stock_submit").addClass('hidden');
                        $("#sell_stock_graph_loading").addClass('hidden');
                        if (json["result"] == "Stock not found") {
                            $("#sell_stock_not_found").removeClass("hidden");
                            $("#sell_stock_graph").addClass("hidden");
                            $("#sell_lineLegend").addClass("hidden");
                            $("#sell_modal_footer").addClass("hidden");
                            $("#stock_sell").addClass("hidden");
                            $("#sell_symbol_title").addClass("hidden");

                        }else if(json["result"] == "success"){
                            symbol = sym;
                            print_sell_results(json);
                        }
                    },
                    error: function (xhr, errmsg, err) {
                        $("#search_stock_submit").button('reset');
                        bootbox.alert('Failed.');
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
}

//Print sell stock results
function print_sell_results(json) {
         var result = json.query.results.quote.reverse();
        symbol = result[result.length-1]["Symbol"].toUpperCase();
        recent_close = result[result.length-1]["Adj_Close"];
        recent_date = result[result.length-1]["Date"];
        shares_owned = json["shares_owned"];
         $("#sell_symbol_title").html(symbol);
         $("#sell_stock_not_found").addClass("hidden");
         $("#sell_symbol_title").removeClass("hidden");
         $("#sell_graph_timescale").removeClass("hidden");
         $("#table_div").removeClass("hidden");
         $("#sell_stock_graph").removeClass("hidden");
         $("#sell_lineLegend").removeClass("hidden");
         $("#sell_modal_footer").removeClass("hidden");
         $("#stock_sell").removeClass("hidden");
         make_graph(result,"sell_stock_graph","sell_lineLegend");
         setup_buysell_text()
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
        $('#'+graph_str).remove(); // this is my <canvas> element
        $('#'+graph_str+'_container').append('<canvas id="'+graph_str+'"><canvas>');
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
            responsive: true,
            animation: false,
            pointDot : false,
            legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend list-unstyled text-center\"><% for (var i=0; i<datasets.length; i++){\%><li><span> <font style=\"color:<%=datasets[i].strokeColor%>\"><%if(datasets[i].label){\%><%=datasets[i].label%><%}%></li><%}%></font></span></ul>"
        };

        var chart = new Chart(stock_graph).Line(stockData, opts);
        $("#"+legend_str).html(chart.generateLegend());
        //legend(document.getElementById(legend_str), stockData);
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
        var s="";
        if (userList[data['symbol']]== undefined) {
            console.log('$("td[data-target=\'#'+data["symbol"]+'td\']").attr("data-target", "#"+target+"div");');
            var t = (data['price'] * data["amount"]);
            $("#clients_stock_tbody").append($.parseHTML('<tr >' +
                '<td class="sort accordion-toggle"  data-toggle="collapse" data-target="#'+data['symbol']+'div" class=""><a id="'+data['symbol']+'a" data-toggle="modal" data-target="#StockModal" data-symbol="'+data['symbol']+'" ><span class="glyphicon glyphicon-search"></span></a> '+data['symbol']+'</td>'+
                '<td class="accordion-toggle" id="'+data['symbol']+'td" data-toggle="collapse" data-target="#'+data['symbol']+'div" >'+data['amount']+'</td>'+
                '<script>'+
                    'var target = ("'+data['symbol']+'").replace(".","");'+
                    '$("td[data-target=\'#'+data["symbol"]+'td\']").attr("id", target+"td");'+

                    '$("td[data-target=\'#'+data["symbol"]+'td\']").attr("data-target", "#"+target+"div");'+
                    '$("td[data-target=\'#'+data["symbol"]+'div\']").attr("data-target", "#"+target+"div");'+
                    '$("#'+data['symbol']+'a").click(function(){'+
                        '$("#stock_symbol").attr("value", "'+data['symbol']+'");'+
                        '$("#search_stock_submit").submit();'+
                    '});'+
                    '$("#'+data['symbol']+'a").attr("id", target+"a");'+
                '</script>'+
                '<td ><button class="btn btn-default btn-xs" data-toggle="modal" data-target="#SellStockModal" data-symbol="'+data["symbol"]+'">Sell</button> </td>'+
                '</tr>' +
                '<tr class="hiddenRow">' +
                '<td colspan="3" class="hiddenRow" >' +
                '<div class="accordian-body collapse" id="'+data["symbol"]+'div">' +
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
                '</script></div></td></tr>'));
            var options ={valueNames: ["buy", "stock", "date", "amount", "price", "total"]};
            userList[data['symbol']] = new List((symbol+"div"),options);
            sell_button_listener();
        }else {
            if (data['buy'] == 'True') {
                s = "<span class='glyphicon glyphicon-chevron-up'></span>Bought"
            } else {
                s = "<span class='glyphicon glyphicon-chevron-down'></span>Sold"
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