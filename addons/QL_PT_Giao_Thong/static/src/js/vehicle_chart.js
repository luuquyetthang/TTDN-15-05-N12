odoo.define('QL_PT_Giao_Thong.vehicle_charts', function(require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        start: function () {
            this._super();
            this.renderBarChart();
            this.renderPieChart();
        },

        renderBarChart: function () {
            var self = this;
            setTimeout(function () { 
                var canvasId = "cot_" + self.record.id;
                var canvas = document.getElementById(canvasId);
        
                if (!canvas) {
                    console.error("❌ Không tìm thấy canvas:", canvasId);
                    return;
                }
        
                console.log("✅ Vẽ biểu đồ cột theo loại xe và tài xế cho:", canvasId);
                var ctx = canvas.getContext('2d');
        
                var vehicleData = self.recordData.vehicle_by_type;
                var driverData = self.recordData.vehicle_by_driver;
        
                console.log("📌 Raw vehicle_by_type data:", vehicleData);
                console.log("📌 Raw vehicle_by_driver data:", driverData);
        
                if (!vehicleData || vehicleData.trim() === "" || !driverData || driverData.trim() === "") {
                    console.error("🚫 vehicle_by_type hoặc vehicle_by_driver bị rỗng hoặc undefined!");
                    return;
                }
        
                try {
                    var jsonStart = vehicleData.indexOf('{');
                    var jsonEnd = vehicleData.lastIndexOf('}') + 1;
        
                    if (jsonStart === -1 || jsonEnd === 0) {
                        throw new Error("Dữ liệu vehicle_by_type không hợp lệ.");
                    }
        
                    vehicleData = vehicleData.substring(jsonStart, jsonEnd);
                    var parsedVehicleData = JSON.parse(vehicleData);
        
                    jsonStart = driverData.indexOf('{');
                    jsonEnd = driverData.lastIndexOf('}') + 1;
        
                    if (jsonStart === -1 || jsonEnd === 0) {
                        throw new Error("Dữ liệu vehicle_by_driver không hợp lệ.");
                    }
        
                    driverData = driverData.substring(jsonStart, jsonEnd);
                    var parsedDriverData = JSON.parse(driverData);
                    if (!parsedVehicleData.labels || !parsedVehicleData.values || 
                        !parsedDriverData.labels || !parsedDriverData.values) {
                        console.error("🚫 Dữ liệu JSON không đúng định dạng!");
                        return;
                    }
                    parsedDriverData.labels = parsedDriverData.labels.map(label => 
                        label === "Kim Snyder" ? "Số lượng xe theo tài xế" : label
                    );
                    var labels = [...parsedVehicleData.labels, ...parsedDriverData.labels];
                    var vehicleValues = parsedVehicleData.values.concat(new Array(parsedDriverData.values.length).fill(0)); 
                    var driverValues = new Array(parsedVehicleData.values.length).fill(0).concat(parsedDriverData.values); 
        
                    var colors = labels.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.6)`);
        
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    label: 'Số lượng xe theo loại',
                                    data: vehicleValues,
                                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1
                                },
                                {
                                    label: 'Số lượng xe theo tài xế',
                                    data: driverValues,
                                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                                    borderColor: 'rgba(255, 99, 132, 1)',
                                    borderWidth: 1
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: { 
                                y: { beginAtZero: true } 
                            }
                        }
                    });
        
                } catch (error) {
                    console.error("🚫 Lỗi khi parse JSON:", error.message);
                }
        
            }, 700); 
        },
        
        renderPieChart: function () {
            var self = this;
            setTimeout(function () { 
                var canvasId = "vehicle_chart_" + self.record.id;
                var canvas = document.getElementById(canvasId);

                if (!canvas) {
                    console.error("❌ Không tìm thấy canvas:", canvasId);
                    return;
                }

                console.log("✅ Vẽ biểu đồ tròn cho:", canvasId);
                var ctx = canvas.getContext('2d');

                var activeVehicles = self.recordData.active_vehicles_int || 0;
                var maintenanceVehicles = self.recordData.maintenance_vehicles_int || 0;
                var availableVehicles = self.recordData.available_vehicles_int || 0;

                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ["Đang hoạt động", "Đang bảo trì", "Chưa hoạt động"],
                        datasets: [{
                            data: [activeVehicles, maintenanceVehicles, availableVehicles],
                            backgroundColor: ["#28a745", "#ffc107", "#17a2b8"],
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                    }
                });
            }, 700); 
        }
    });
});
