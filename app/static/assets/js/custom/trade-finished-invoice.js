/**
 * Created by marco on 2017/12/29.
 */
var TableData = function() {
    "use strict";
    var runDataTable_invoice = function(data_per_page, arr_summary_info){
        var addd = 0;
        var table = $("#table-invoice").DataTable({
                "orderClasses": true,   // 高亮显示表格中排序的列。
                "pageLength": data_per_page,
                "processing": true,     // 是否显示处理状态(排序的时候，数据很多耗费时间长的话，也会显示这个)。
                "serverSide": false,    // 是否开启服务器模式
                "searching": true,      // 开启全局搜索
                // "columns":[
                //     { "data": null },
                //     { "data": "item" },
                //     { "data": "description" },
                //     { "data": "quantity" },
                //     { "data": "unit_cost" },
                //     { "data": "goods_amount" },
                //     { "data": "post_amount" },
                //     { "data": "total" }
                // ],
                // 由于第 0 列是行号，排序和搜索没有意义，所以禁用第 0 列的搜索和排序。
                "columnDefs": [
                    {
                        "targets": 0,
                        "searchable": false,
                        "orderable": false,
                        "defaultContent": ""
                    }//,
                    // {
                    //     "targets": 2,   // description
                    //     "class": "hidden-480"
                    // },
                    // {
                    //     "targets": 3,   // quantity
                    //     "class": "hidden-480"
                    // },
                    // {
                    //     "targets": 4,   // unit_cost
                    //     "class": "hidden-480"
                    // }
                ],
                // 因为 DT 默认会设置第 0 列升序排列。由于前面已经禁用，因此改为设置默认的排序列为第 1 列。
                "order": [[1, "asc"]],
                "lengthMenu": [ [10, 25, 50, 75, 100, -1], [10, 25, 50, 75, 100, "All"] ],
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
                // "rowCallback": function(row, data, index) {
                //     // if(index==0) addd=0;
                //     var x = parseFloat(data[3]);
                //     addd += parseFloat(x);  // 第几列
                //     // $("#weightsum").html(formatFloat(addd,3));
                //     $("#weightsum").html(addd);
                //     return row;
                // },
                "drawCallback": function(settings){
                    var api = this.api();
                    var startIndex= api.context[0]._iDisplayStart;  // 获取到本页开始的条数
                    api.column(0).nodes().each(function(cell, i) {
                        cell.innerHTML = "<b>" + (startIndex + i + 1) + "</b>";
                    });

                    $("#table-invoice_paginate").append("  到第 <input style='height:28px;line-height:28px;width:40px;' class='margin text-center' id='changePage' type='text'> 页  <a class='btn btn-default shiny' style='margin-bottom:5px' href='javascript:void(0);' id='dataTable-btn'>确认</a>");
                    var oTable = $("#sample_1").dataTable();
                    $("#dataTable-btn").click(function(e) {
                        if($("#changePage").val() && $("#changePage").val() > 0) {
                            var redirectpage = $("#changePage").val() - 1;
                        } else {
                            var redirectpage = 0;
                        }
                        oTable.fnPageChange(redirectpage);
                        //oTable.page(redirectpage).draw(false);
                    });
                },
                "footerCallback": function( tfoot, data, start, end, display ) {
                    // var i;
                    // var subtotal=0;
                    // for ( i=start ; i<end ; i++ ) {
                    //     subtotal += parseFloat(data[3]);
                    // }

                    // 这里不是DataTable初始化，通过api()，达到一样的效果。
                    var api = this.api();
                    // $( api.column(3).footer() ).html(subtotal);
                    for (var index=0; index<arr_summary_info.length; index++) {
                        // reduce 处理一条记录有问题。因此需要对一条记录的情况单独处理。
                        if (data.length > 1) {
                            $( api.column(arr_summary_info[index].idx).footer() ).html(
                                "<b>" +
                                // 遍历第 x 列的数据。reduce() 方法遍历结果集，通过回调函数返回从左到右的数据
                                api.column(arr_summary_info[index].idx).data().reduce( function ( a, b ) {
                                    return parseFloat(a) + parseFloat(b);
                                } ).toFixed(arr_summary_info[index].fixed)
                                + "</b>"
                            );
                        }
                        else {
                            $( api.column(arr_summary_info[index].idx).footer() ).html(
                                "<b>" + data[0][arr_summary_info[index].idx] + "</b>"
                            );
                        }
                    }
                    // $( api.column(3).footer() ).html(
                    //     "<b>" +
                    //     // 遍历第 3 列的数据。reduce() 方法遍历结果集，通过回调函数返回从左到右的数据
                    //     api.column(3).data().reduce( function ( a, b ) {
                    //         return parseFloat(a) + parseFloat(b);
                    //     } ).toFixed(4)
                    //     + "</b>"
                    // );
                    // $( api.column(5).footer() ).html(
                    //     "<b>" +
                    //     api.column(5).data().reduce( function ( a, b ) {
                    //         return parseFloat(a) + parseFloat(b);
                    //     } ).toFixed(2)
                    //     + "</b>"
                    // );
                    // $( api.column(6).footer() ).html(
                    //     "<b>" +
                    //     api.column(6).data().reduce( function ( a, b ) {
                    //         return parseFloat(a) + parseFloat(b);
                    //     } ).toFixed(2)
                    //     + "</b>"
                    // );
                    // $( api.column(7).footer() ).html(
                    //     "<b>" +
                    //     api.column(7).data().reduce( function ( a, b ) {
                    //         return parseFloat(a) + parseFloat(b);
                    //     } ).toFixed(2)
                    //     + "</b>"
                    // );
                }
        });
    };
    return {
        // main function to initiate template pages
        init : function(data_per_page, arr_summary_info) {
            runDataTable_invoice(data_per_page, arr_summary_info);
        }
    }
}();