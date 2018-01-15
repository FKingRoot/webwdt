var TableData = function() {
    "use strict";
    var opts = {
        "orderClasses": true,   // 高亮显示表格中排序的列。
        "processing": true,     // 是否显示处理状态(排序的时候，数据很多耗费时间长的话，也会显示这个)。
        "columns":[
            { "data": null },
            { "data": null },
            { "data": "log_time" },
            { "data": "handle_flag" },
            { "data": "total_count" },
            { "data": "start_time" },
            { "data": "end_time" },
            { "data": "message" }
        ],
        // 由于第 0 列是展开按钮，第 1 列是行号，排序和搜索没有意义，所以禁用第 0 列和第 1 列的搜索和排序。
        "columnDefs": [
            {   "targets": 0,
                "searchable": false,
                "orderable": false,
                "class": "center details-control",
                "defaultContent": ""
            }
            ,{  "targets": 1,
                "searchable": false,
                "orderable": false,
                "class": "center"
            }
            ,{  "targets": 3,   // handle_flag
                "class": "center hidden-xs",
                "render": function (data, type, row, meta) {
                    return "<span class='label label-sm "
                        + (data ? "label-success" : "label-danger")
                        + "'>" + data + "</span>";
                }
            }
            ,{  "targets": 7,   // message
                "class": "hidden-xs"
            }
        ],
        // 定义 DataTables 的组件元素的显示和显示顺序。
        //  1. `l` 代表 length，左上角的改变每页显示条数控件
        //  2. `f` 代表 filtering，右上角的过滤搜索框控件
        //  3. `t` 代表 table，表格本身
        //  4. `i` 代表 info，左下角的表格信息显示控件
        //  5. `p` 代表 pagination，右下角的分页控件
        //  6. `r` 代表 processing，表格中间的数据加载等待提示框控件
        //  7. `B` 代表 button，Datatables可以提供的按钮控件，默认显示在左上角
        // DataTables 自定义标签：
        //  1. < > - 这个尖括号就代表 html标签里的  <div></div>
        //  2. <"className" > - 代表添加了class的div  <div class="className"></div>
        //  3. <"#id" > - 代表添加了id的div <div id="id"></div>
        "dom": "lrf<'#gbtn-export.col-sm-6'>tip",
        // 因为 DT 默认会设置第 1 列升序排列。由于前面已经禁用，因此改为设置默认的排序列为第 2 列。
        "order": [[2, "asc"]],
        // "lengthMenu": [ [10, 25, 50, 75, 100, -1], [10, 25, 50, 75, 100, "All"] ],
        "language": {
            "aria": {
                "sortAscending":  ": 以升序排列此列",
                "sortDescending": ": 以降序排列此列"
            },
            "processing": "处理中...",
            "lengthMenu": "每页 _MENU_ 条记录",
            "zeroRecords": "没有查询到记录",
            "info": "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
            "infoEmpty": "无记录",
            "search": "搜索：",
            "infoFiltered": "(从 _MAX_ 条记录过滤)",
            "loadingRecords": "正在加载数据--请等待...",
            "emptyTable": "未有相关数据",
            "url": "",
            "infoThousands": ",",
            "paginate": {
                "first": "首页",
                "previous": "上一页",
                "next": "下一页",
                "last": "尾页 "
            }
        },
        // if your datatable is too long to load (huge table in html for example),
        // You may have to use initComplete to prevent this,
        // since the div.toolbar node may not exist yet when $('div.toolbar').html is called.
        "initComplete": function(settings, json){
            var api = new $.fn.dataTable.Api( settings );
            if ( api.data().length>0 || json != undefined ) {
                $("div[id='gbtn-export']").html(
                    "<div class='btn-group'>"
                        + "<a class='btn btn-azure' href='javascript:;'>"
                            + "<!--data-placement='top' data-toggle='tooltip' data-original-title='print the data.'>-->"
                            + "<i class='fa fa-print'></i>"
                        + "</a>"
                        + "<button type='button' class='btn btn-azure'>"
                            + "<!--data-placement='top' data-toggle='tooltip' data-original-title='export data in a specified format.'>-->"
                            + "Export"
                        + "</button>"
                        + "<button type='button' class='btn btn-azure dropdown-toggle' data-toggle='dropdown' aria-expanded='true'>"
                            + "<span class='caret'></span>"
                        + "</button>"
                        + "<ul class='dropdown-menu dropdown-light pull-right' role='menu'>"
                            + "<li>"
                                + "<a href='javascript:;'>"
                                    + "<i class='fa fa-file-code-o'> .json</i>"
                                + "</a>"
                            + "</li>"
                            + "<li>"
                                // + "<a href='{{ url_for(''main.exec_plan_export_xls'')}}'>"
                                + "<a href='javascript:;'>"
                                    + "<i class='fa fa-file-excel-o'> .xls</i>"
                                + "</a>"
                            + "</li>"
                            + "<li>"
                                + "<a href='javascript:;'>"
                                    + "<i class='fa fa-file-text-o'> .csv</i>"
                                + "</a>"
                            + "</li>"
                            + "<li>"
                                + "<a href='javascript:;'>"
                                    + "<i class='fa fa-file-pdf-o'> .pdf</i>"
                                + "</a>"
                            + "</li>"
                        + "</ul>"
                    + "</div>");
            }
        },
        "createdRow": function(row, data, dataIndex) {  // 在 rowCallback 之前执行。
            if (!data.handle_flag) {
                $(row).addClass("danger");
            }

            // 如果没有明细数据，不显示展开内容。
            if (data.total_count<=0) {
                $("td", row).eq(0).removeClass("details-control");
            }
        }
    };
    var table;

    // https://datatables.net/examples/server_side/pipeline.html
    // 由于每次绘制请求都需要向服务器发起一个 Ajax 调用，服务器端的处理会承受很大的压力。
    // 在一个拥有大量页面浏览量的站点，你的服务器甚至有可能被自己应用产生的DDos攻击拖垮。
    // 可以通过缓存比每次绘制所需要的更多的数据来减少对服务器的 Ajax 调用次数。
    // 这是通过拦截 Ajax 调用，并通过数据缓存控制进行路由来实现的; 
    // 如果缓存的数据可用，则使用来自缓存的数据；否则发出 Ajax 请求。
    // 对 Ajax 请求的拦截是通过设定一个函数作为 ajax option 选项来完成的。该函数随后将执行一个判断逻辑，决定是需要另一个 Ajax 调用的逻辑，还是使用来自缓存的数据。
    // 请记住，此缓存仅用于分页; 若需要进行例如排序和搜索等其他交互，则必须清除流水线，因为使用服务器端处理的完整数据集仅在服务器上可用。

    //
    // Pipelining function for DataTables. To be used to the `ajax` option of DataTables
    // 用于 DataTables 的流水线函数。
    //
    $.fn.dataTable.pipeline = function ( opts ) {
        // Configuration options
        var conf = $.extend( {
            pages: 5,       // number of pages to cache
            url: "",        // script url
            data: null,     // function or object with parameters to send to the server
                            // matching how `ajax.data` works in DataTables
            method: "POST"   // Ajax HTTP method
        }, opts );
    
        // Private variables for storing the cache
        var cacheLower = -1;
        var cacheUpper = null;
        var cacheLastRequest = null;
        var cacheLastJson = null;
    
        return function ( request, drawCallback, settings ) {
            var ajax          = false;
            var requestStart  = request.start;
            var drawStart     = request.start;
            var requestLength = request.length;
            var requestEnd    = requestStart + requestLength;
            
            if ( settings.clearCache ) {
                // API requested that the cache be cleared
                ajax = true;
                settings.clearCache = false;
            }
            else if ( cacheLower < 0 || requestStart < cacheLower || requestEnd > cacheUpper ) {
                // outside cached data - need to make a request
                ajax = true;
            }
            else if ( JSON.stringify( request.order ) !== JSON.stringify( cacheLastRequest.order ) ||
                    JSON.stringify( request.columns ) !== JSON.stringify( cacheLastRequest.columns ) ||
                    JSON.stringify( request.search )  !== JSON.stringify( cacheLastRequest.search )
            ) {
                // properties changed (ordering, columns, searching)
                ajax = true;
            }
            
            // Store the request for checking next time around
            cacheLastRequest = $.extend( true, {}, request );
    
            if ( ajax ) {
                // Need data from the server
                if ( requestStart < cacheLower ) {
                    requestStart = requestStart - (requestLength*(conf.pages-1));
    
                    if ( requestStart < 0 ) {
                        requestStart = 0;
                    }
                }
                
                cacheLower = requestStart;
                cacheUpper = requestStart + (requestLength * conf.pages);
    
                request.start = requestStart;
                request.length = requestLength*conf.pages;
    
                // Provide the same `data` options as DataTables.
                if ( $.isFunction ( conf.data ) ) {
                    // As a function it is executed with the data object as an arg
                    // for manipulation. If an object is returned, it is used as the
                    // data object to submit
                    var d = conf.data( request );
                    if ( d ) {
                        $.extend( request, d );
                    }
                }
                else if ( $.isPlainObject( conf.data ) ) {
                    // As an object, the data given extends the default
                    $.extend( request, conf.data );
                }
    
                settings.jqXHR = $.ajax( {
                    "type":     conf.method,
                    "url":      conf.url,
                    "data":     request,
                    "dataType": "json",
                    "cache":    false,
                    "success":  function ( json ) {
                        cacheLastJson = $.extend(true, {}, json);
    
                        if ( cacheLower != drawStart ) {
                            json.data.splice( 0, drawStart-cacheLower );
                        }
                        if ( requestLength >= -1 ) {
                            json.data.splice( requestLength, json.data.length );
                        }
                        
                        drawCallback( json );
                    }
                } );
            }
            else {
                json = $.extend( true, {}, cacheLastJson );
                json.draw = request.draw;   // Update the echo for each response
                json.data.splice( 0, requestStart-cacheLower );
                json.data.splice( requestLength, json.data.length );
    
                drawCallback(json);
            }
        }
    };
    
    // Register an API method that will empty the pipelined data, forcing an Ajax
    // fetch on the next draw (i.e. `table.clearPipeline().draw()`)
    $.fn.dataTable.Api.register( "clearPipeline()", function () {
        return this.iterator( "table", function ( settings ) {
            settings.clearCache = true;
        } );
    } );

	var runDataTable_trade_finished_server = function(ajax_url, data_per_page, logtime_start, logtime_end, handled) {
        opts["pageLength"] = data_per_page;
        opts["serverSide"] = true;  // 开启服务器模式
        opts["searching"] = false;  // 关闭全局搜索

        opts["ajax"] = $.fn.dataTable.pipeline( {
            url: ajax_url,
            type: "POST",
            data: {
                "ajax_start_time": logtime_start,
                "ajax_end_time": logtime_end,
                "ajax_handled": handled
            },
            pages: 5 // number of pages to cache
        } )
        // opts["ajax"] = {
        //     url: ajax_url,
        //     type: "POST",
        //     data: {
        //         "ajax_start_time": logtime_start,
        //         "ajax_end_time": logtime_end,
        //         "ajax_handled": handled
        //     }
        // };
        opts["drawCallback"] =
            function(settings){
                // 注意，后端分页和前端分页处理方式不同。
                var api = this.api();
                var startIndex = api.context[0]._iDisplayStart;  // 获取到本页开始的条数
                api.column(1).nodes().each(function(cell, i) {
                    cell.innerHTML = "<b>" + (startIndex + i + 1) + "</b>";
                });

                $("#sample_1_paginate").append("  到第 <input style='height:28px;line-height:28px;width:40px;' class='margin text-center' id='changePage' type='text'> 页  <a class='btn btn-default shiny' style='margin-bottom:5px' href='javascript:void(0);' id='dataTable-btn'>确认</a>");
                var oTable = $("#sample_1").dataTable();
                $("#dataTable-btn").click(function(e) {
                    if($("#changePage").val() && $("#changePage").val() > 0) {
                        var redirectpage = $("#changePage").val() - 1;
                    } else {
                        var redirectpage = 0;
                    }
                    oTable.fnPageChange(redirectpage);
                });
            };

        var table = $("#sample_1")
            .on("preXhr.dt", function ( e, settings, data ) {
                $("#loading_modal").modal("show");
            })
            .on("xhr.dt", function ( e, settings, json, xhr ) {
                $("#loading_modal").modal("hide");
            })
            .on("error.dt", function ( e, settings, techNote, message ) {
                // 页面出错，要退出 loading 状态。
                $("#loading_modal").modal("hide");
            })
            .DataTable(opts);
	};

	var runDataTable_trade_finished_client = function(data, data_per_page) {
        opts["pageLength"] = data_per_page;
        opts["serverSide"] = false; // 关闭服务器模式
        opts["searching"] = true;   // 开启全局搜索
        opts["data"] = data;
        opts["drawCallback"] =
            function(settings){
                // 注意，后端分页和前端分页处理方式不同。
                var api = this.api();
                api.column(1).nodes().each(function(cell, i) {
                    cell.innerHTML = "<b>" + (i + 1) + "</b>";
                });

                $("#sample_1_paginate").append("  到第 <input style='height:28px;line-height:28px;width:40px;' class='margin text-center' id='changePage' type='text'> 页  <a class='btn btn-default shiny' style='margin-bottom:5px' href='javascript:void(0);' id='dataTable-btn'>确认</a>");
                var oTable = $("#sample_1").dataTable();
                $("#dataTable-btn").click(function(e) {
                    if($("#changePage").val() && $("#changePage").val() > 0) {
                        var redirectpage = $("#changePage").val() - 1;
                    } else {
                        var redirectpage = 0;
                    }
                    oTable.fnPageChange(redirectpage);
                });
            };

        table = $("#sample_1").DataTable(opts);
    }

    function format ( d ) {
        // `d` is the original data object for the row
        var tr_html = "";
        for (var i=0; i<d.trades.length; i++) {
            var x = Flask.url_for("main.trade_finished_invoice", {"id": d.trades[i].trade_id});
            tr_html +=
            "<tr>"+
                "<th class='center'>"+(i+1)+"</th>"+
                "<td><a href='" + x + "' target='_blank'>"+d.trades[i].trade_id+"</a></td>"+
                "<td>"+d.trades[i].receiver_name+"</td>"+
                "<td class='text-right'>"+d.trades[i].goods_count+"</td>"+
                "<td class='text-right'>"+d.trades[i].paid+"</td>"+
                "<td>"+d.trades[i].created+"</td>"+
                "<td>"+d.trades[i].modified+"</td>"+
            "</tr>"
        }

        return "<table class='table table-condensed table-hover' id='nested_table_1'>" +
                "<thead>" +
                    "<tr>" +
                        "<th class='center'>#</th>" +
                        "<th>Trade Id</th>" +
                        "<th>Receiver Name</th>" +
                        "<th class='hidden-xs'>Goods Count</th>" +
                        "<th>Goods Amount</th>" +
                        "<th>Created Date</th>" +
                        "<th class='hidden-xs'>Modified Date</th>" +
                    "</th>" +
                "</thead>" +
                "<tbody>" +
                    tr_html +
                "</tbody>" +
        "</table>";
    }

    // Add event listener for opening and closing details
    $("#sample_1 tbody").on("click", "td.details-control", function () {
        var tr = $(this).closest("tr");
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass("shown");
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass("shown");
        }
    });

	return {
		//main function to initiate template pages
		// init : function(exec_mode, data, ajax_url, data_per_page, logtime_start, logtime_end, handled) {
        init : function(exec_mode, data, ajax_url, data_per_page, logtime_start, logtime_end, handled) {
		    if ( exec_mode == "1" ) {
		        runDataTable_trade_finished_client(data, data_per_page);
            }
            else
		    if ( exec_mode == "2" ) {
			    runDataTable_trade_finished_server(ajax_url, data_per_page, logtime_start, logtime_end, handled);
            }
		}
	};
}();