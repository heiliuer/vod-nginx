/**
 * Created by Heiliuer on 2016/11/17 0017.
 */

$.get("files.json", function (datas) {
    if (typeof datas == "string") {
        datas = JSON.parse(datas)
    }
    initApp(datas)
})


function initApp(datas) {

    var local_histories = (localStorage.getItem("histories") || "").split("###");
    var histories = new Set(local_histories);

    var showAction = function () {
        var buttons1 = [
            {
                text: '搜索历史',
                label: true
            }
        ];
        histories.forEach(function (key) {
            buttons1.push({
                text: key,
                onClick: function () {
                    vm.search(key);
                }
            })
        });

        var buttons2 = [
            {
                text: '清除',
                onClick: function () {
                    clearHistory();
                }
            }
        ];

        var buttons3 = [
            {
                text: '取消',
                bg: 'danger'
            }
        ];
        var groups = [buttons1, buttons2, buttons3];
        $.actions(groups);
    }

    var showItemKeysAction = function (name) {
        var buttons1 = [
            {
                text: '选择关键字',
                label: true
            }
        ];

        var keys = name.split(/-|:|\./);

        keys.forEach(function (key) {
            if (key != "") {
                buttons1.push({
                    text: key,
                    onClick: function () {
                        vm.search(key);
                        $('[href="#tab_search"]').click().click();
                    }
                })
            }
        });


        var buttons3 = [
            {
                text: '取消',
                bg: 'danger'
            }
        ];
        var groups = [buttons1, buttons3];
        $.actions(groups);
    }

    function storeHistories() {
        localStorage.setItem("histories", Array.from(histories).join("###"))
    }

    function addHistory(key) {
        histories.add(key);
        storeHistories();
    }

    function clearHistory() {
        histories.clear();
        storeHistories();
    }


    var searchData = JSON.parse(JSON.stringify(datas));

    var video = document.querySelectorAll('#video')[0];
    var vm = new Vue({
        el: "#app",
        data: {
            /*host: location.protocol + "//" + location.hostname + ":7777/",*/
            host: "/",
            datas: datas,
            cFile: null,
            searchKey: ""
        },
        methods: {
            showItemKeysAction: showItemKeysAction,
            showAction: showAction,
            refresh: function (data, file) {
                var url = this.host + data.uid + '/' + file.path;
                video.src = url;
                document.title = file.name
                cFile = file
                setTimeout(function () {
                    video.play();
                }, 200);
            },
            clear: function () {
                this.searchKey = "";
            },
            search: function (key) {
                this.searchKey = key;
            }
        },
        computed: {
            playUid: function () {
                return this.cFile ? this.cFile.uid : "";
            },
            searchFiles: function () {
                console.log("change searchKey:",this.searchKey);
                var that = this;
                document.querySelector('#search').blur();
                if (this.searchKey) {
                    addHistory(this.searchKey);
                    that.datas.forEach(function (data, index) {
                        var files = [];
                        data.files.forEach(function (file) {
                            if (file.name.indexOf(that.searchKey) != -1) {
                                files.push(file);
                                console.log("find file:",file.name);
                            }
                        });
                        searchData[index].files = files;
                    });

                    return searchData;
                } else {
                    return this.datas;
                }
            }
        },
        ready: function () {
            $.init();
        }
    })
}
