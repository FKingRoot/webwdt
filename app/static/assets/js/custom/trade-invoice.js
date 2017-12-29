/**
 * Created by marco on 2017/12/29.
 */
var TableData = function(data_per_page, data) {
    "use strict";
    var runDataTable_invoice = function(){
        var table = $("#table-invoice").DataTable({
// 由于第 0 列是行号，排序和搜索没有意义，所以禁用第 0 列的搜索和排序。
                                    "columnDefs": [{
                                        "searchable": false,
                                        "orderable": false,
                                        "targets": 0
                                    }],
                                    // 因为 DT 默认会设置第 0 列升序排列。由于前面已经禁用，因此改为设置默认的排序列为第 1 列。
                                    "order": [[1, 'asc']],
                                    "drawCallback": function(){
                                        var api = this.api();
                                        //var startIndex= api.context[0]._iDisplayStart;    // 获取到本页开始的条数
                                        api.column(0).nodes().each(function(cell, i) {
                                            //cell.innerHTML = startIndex + i + 1;
                                            cell.innerHTML = i + 1;
                                        });
                                    }
                // "orderClasses": true,   // 高亮显示表格中排序的列。
                // "pageLength": data_per_page,
                // "processing": true,     // 是否显示处理状态(排序的时候，数据很多耗费时间长的话，也会显示这个)。
                // "serverSide": false,    // 是否开启服务器模式
                // "searching": true,     // 开启全局搜索
                // //"data": data,
                // "columns":[
                //     { "data": null },
                //     { "data": "item" },
                //     { "data": "description" },
                //     { "data": "quantity" },
                //     { "data": "unit_cost" },
                //     { "data": "total" }
                // ],
                // 由于第 0 列是行号，排序和搜索没有意义，所以禁用第 0 列的搜索和排序。
                // "columnDefs": [
                //     {
                //         "targets": 0,
                //         "searchable": false,
                //         "orderable": false,
                //         "defaultContent": ""
                //     },
                //     {
                //         "targets": 2,   // description
                //         "class": "hidden-480"//,
                //         // "render": function (data, type, row, meta) {
                //         //     return "<span class='label label-sm " + (data ? "label-success" : "label-danger") + "'>" + data + "</span>";
                //         // }
                //     },
                //     {
                //         "targets": 3,   // quantity
                //         "class": "hidden-480"
                //     },
                //     {
                //         "targets": 4,   // unit_cost
                //         "class": "hidden-480"
                //     }
                // ],
                // // 因为 DT 默认会设置第 0 列升序排列。由于前面已经禁用，因此改为设置默认的排序列为第 1 列。
                // "order": [[1, "asc"]],
                // "lengthMenu": [ [10, 25, 50, 75, 100, -1], [10, 25, 50, 75, 100, "All"] ],
                // "language": {
                //     "aria": {
                //         "sortAscending":  ": 以升序排列此列",
                //         "sortDescending": ": 以降序排列此列"
                //     },
                //     "processing": "处理中...",
                //     "lengthMenu": "每页 _MENU_ 条记录",
                //     "zeroRecords": "没有查询到记录",
                //     "info": "当前显示第 _START_ 至 _END_ 项，共 _TOTAL_ 项。",
                //     "infoEmpty": "无记录",
                //     "search": "搜索：",
                //     "infoFiltered": "(从 _MAX_ 条记录过滤)",
                //     "loadingRecords": "正在加载数据--请等待...",
                //     "emptyTable": "未有相关数据",
                //     "url": "",
                //     "infoThousands": ",",
                //     "paginate": {
                //         "first": "首页",
                //         "previous": "上一页",
                //         "next": "下一页",
                //         "last": "尾页 "
                //     }
                // }//,
                // "createdRow": function(row, data, dataIndex) {  // 在 rowCallback 之前执行。
                //     //var $btnBuy  =  $('<button class="buy">购买</button>');
                //     //var $btnLook =  $('<button class="look">查看</button>');
                //     //$("td", row).eq(6).append($btnBuy).append($btnLook);
                //     //if (!$("td", row).eq(3)) {
                //     if (!data.handle_flag) {
                //         $(row).addClass("danger");
                //     }
                //
                //     // 如果没有明细数据，不显示展开内容。
                //     if (data.total_count<=0) {
                //         //$("td", row).eq(0).css("background", "");
                //         $("td", row).eq(0).removeClass("details-control");
                //     }
                // },
                //"rowCallback": function(row, data, index) {
                //    // 每行中的时间列, 全局变量
                //    createTime = new Date(aData.createTime);    //后台返回的时间戳
                //    var year  = createTime.getFullYear()+'年';
                //    var month = createTime.getMonth()+1+'月';
                //    var date  = createTime.getDate()+'日'+createTime.getHours()+'时'+createTime.getMinutes()+'分'+createTime.getSeconds()+'秒';
                //    $('td:eq(5)', nRow).html(year+month+date);  //设置该列的值
                //
                //    // 每行中的状态列  该状态进行判断 并设置相关的列值
                //    var sellstatus = aData.sellstatus;
                //    if (sellstatus==2) {    // 使用权交易
                //        var num = aData.usemoney;
                //        $('td:eq(2)', nRow).html(num);  //设置该列的值
                //    }
                //    if (sellstatus==3) {    // 所有权交易
                //        var num = aData.allmoney;
                //        $('td:eq(2)', nRow).html(num);  //设置该列的值
                //    }
                //},
                // "drawCallback": function(settings){
                //     var api = this.api();
                //     var startIndex= api.context[0]._iDisplayStart;  // 获取到本页开始的条数
                //     api.column(1).nodes().each(function(cell, i) {
                //         cell.innerHTML = "<b>" + (startIndex + i + 1) + "</b>";
                //     });
                //
                //     $("#sample_1_paginate").append("  到第 <input style='height:28px;line-height:28px;width:40px;' class='margin text-center' id='changePage' type='text'> 页  <a class='btn btn-default shiny' style='margin-bottom:5px' href='javascript:void(0);' id='dataTable-btn'>确认</a>");
                //     var oTable = $("#sample_1").dataTable();
                //     $("#dataTable-btn").click(function(e) {
                //         if($("#changePage").val() && $("#changePage").val() > 0) {
                //             var redirectpage = $("#changePage").val() - 1;
                //         } else {
                //             var redirectpage = 0;
                //         }
                //         oTable.fnPageChange(redirectpage);
                //         //oTable.page(redirectpage).draw(false);
                //     });
                // }
        });
    };
    return {
        // main function to initiate template pages
        init : function() {
            runDataTable_invoice();
        }
    }
}();