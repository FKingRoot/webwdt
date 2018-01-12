/**
 * Created by marco on 2017/12/29.
 */
var TableData = function() {
    "use strict";
    var runDataTable_invoice = function(data_per_page){
        var table = $("#table-invoice").DataTable({
                "orderClasses": true,   // 高亮显示表格中排序的列。
                "pageLength": data_per_page,
                "processing": true,     // 是否显示处理状态(排序的时候，数据很多耗费时间长的话，也会显示这个)。
                "serverSide": false,    // 关闭服务器模式
                "searching": true,      // 开启全局搜索
                // 由于第 0 列是行号，排序和搜索没有意义，所以禁用第 0 列的搜索和排序。
                "columnDefs": [
                    {
                        "targets": 0,
                        "searchable": false,
                        "orderable": false,
                        "defaultContent": ""
                    }
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
                "drawCallback": function(settings){
                    // 注意，后端分页和前端分页处理方式不同。
                    var api = this.api();
                    api.column(1).nodes().each(function(cell, i) {
                        cell.innerHTML = "<b>" + (i + 1) + "</b>";
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
                    // 这里不是DataTable初始化，通过api()，达到一样的效果。
                    var api = this.api();
                    // $( api.column(3).footer() ).html(subtotal);
                    // reduce 处理一条记录有问题。
                    $( api.column(3).footer() ).html(
                        "<b>" +
                        // 遍历第 3 列的数据。reduce() 方法遍历结果集，通过回调函数返回从左到右的数据
                        api.column(3).data().reduce( function ( a, b ) {
                            return parseFloat(a) + parseFloat(b);
                        } ).toFixed(4)
                        + "</b>"
                    );
                    $( api.column(5).footer() ).html(
                        "<b>" +
                        api.column(5).data().reduce( function ( a, b ) {
                            return parseFloat(a) + parseFloat(b);
                        } ).toFixed(2)
                        + "</b>"
                    );
                    $( api.column(6).footer() ).html(
                        "<b>" +
                        api.column(6).data().reduce( function ( a, b ) {
                            return parseFloat(a) + parseFloat(b);
                        } ).toFixed(2)
                        + "</b>"
                    );
                    $( api.column(7).footer() ).html(
                        "<b>" +
                        api.column(7).data().reduce( function ( a, b ) {
                            return parseFloat(a) + parseFloat(b);
                        } ).toFixed(2)
                        + "</b>"
                    );
                }
        });
    };
    return {
        // main function to initiate template pages
        init : function(data_per_page) {
            runDataTable_invoice(data_per_page);
        }
    }
}();