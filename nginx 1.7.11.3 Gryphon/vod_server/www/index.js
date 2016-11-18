/**
 * Created by Heiliuer on 2016/11/17 0017.
 */

$.get("files.json", function (datas) {
    if (typeof datas == "string") {
        datas = JSON.parse(datas)
    }
    console.log(datas)
    initApp(datas)
})


function initApp(datas) {
    new Vue({
        el: "#app",
        data: {
            /*host: location.protocol + "//" + location.hostname + ":7777/",*/
            host: "/",
            datas: datas
        },
        methods: {
            refresh: function (data, file) {
                var url = this.host + data.uid + '/' + file;
                console.log(url)
                document.querySelectorAll('#video')[0].src = url;
                document.title = file
            }
        },
        ready: function () {
            $.init();
        }
    })
}
