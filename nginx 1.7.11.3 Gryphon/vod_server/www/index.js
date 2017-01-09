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

    function showAbout() {
        $.modal({
            title: '扫码分享此网址',
            text: '<img width="200" height="200" src="http://qr.liantu.com/api.php?text=' + location.href + '"> <br/> © 2016 heiliuer',
            buttons: [
                {
                    text: '确定',
                    onClick: function () {
                    }
                }
            ]
        })
    }


    var searchData = JSON.parse(JSON.stringify(datas));

    Vue.component("list", {
        template: "#list-compo",
        props: ["data", "files", "playUid"],
        methods: {
            showImg: function (img) {
                $.photoBrowser({
                    photos: [img],
                    type: 'popup'
                }).open();
            },
            showItemKeysAction: showItemKeysAction,
            refresh: function (data, file, $event) {
                vm.refresh(data, file, $event);
            }
        }
    })

    var video = document.querySelectorAll('#video')[0];
    video.addEventListener("ended", function () {
        if ($nextLi.length) {
            $nextLi.find(".item-title").click();
        }
    }, false);
    var $nextLi = $([])
    var vm = new Vue({
        el: "#app",
        data: {
            /*host: location.protocol + "//" + location.hostname + ":7777/",*/
            host: "/",
            datas: datas,
            cFile: null,
            searchKey: "",
            searchFiles: searchData
        },
        methods: {
            showAbout: showAbout,
            showAction: showAction,
            refresh: function (data, file, $event) {
                var url = this.host + data.uid + '/' + file.path;
                video.src = url;
                document.title = file.name;
                this.cFile = file;
                // console.log(this.cFile);
                setTimeout(function () {
                    video.play();
                }, 200);

                var $li = $($event.target).parents("li");
                $nextLi = $li.next("li");
                if (!$nextLi.length) {
                    $nextLi = $li.parents("ul").next("ul").find("li");
                    if (!$nextLi.length) {
                        $nextLi = $li.parents("ul").siblings("ul").find("li").first();
                    }
                }
                // console.log("next:", $nextLi);
            },
            clear: function () {
                this.searchKey = "";
            },
            search: function (key) {
                this.searchKey = key;
            }

        },
        watch: {
            "searchKey": function (key) {
                console.log("change searchKey:", key);
                var that = this;
                document.querySelector('#search').blur();
                if (key) {
                    addHistory(key);
                    that.datas.forEach(function (data, index) {
                        var files = [];
                        data.files.forEach(function (file) {
                            if (file.name.indexOf(key) != -1) {
                                files.push(file);
                            }
                        });
                        that.searchFiles[index].files = files;
                    });
                } else {
                    that.datas.forEach(function (data, index) {
                        that.searchFiles[index].files = data.files;
                    });
                }
            }
        },
        computed: {
            playUid: function () {
                return this.cFile ? this.cFile.uid : "";
            }
        },
        ready: function () {
            $.init();
        }
    })
}
