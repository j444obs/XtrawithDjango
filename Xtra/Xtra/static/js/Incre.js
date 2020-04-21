// 采用ES6语法
// 创建Vue对象vm
let vm = new Vue({
    el: '#app',     // 通过ID选择器找到绑定的HTML内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data:{      // 数据对象
        // v-model
        allow:'',
        userdatabases:[],
        userbackupinfos:[],

        // v-show
        error_allow:false,
    },

        mounted() {
        // 获取数据
        this.get_userdatabases();
        this.get_userbackups();
    },

    methods:{  // 定义和实现事件方法
        get_userbackups(){
            let url = '/userbackups/';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.userbackupinfos = response.data.userbackupinfos;
                    } else {
                        console.log(response.data);
                        this.userbackupinfos = [];
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.userbackupinfos = [];
                })
        },

                get_userdatabases(){
            let url = '/userdatabases/';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        this.userdatabases = response.data.userdatabases;
                    } else {
                        console.log(response.data);
                        this.userdatabases = [];
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.userdatabases = [];
                })
        },


        // 检验是否勾选协议
        check_allow(){
            if (!this.allow){
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        // 监听表单提交事件
        on_submit(){
            this.check_allow();
            // 在校验之后，注册数据中，只要有错误，就禁用掉表单的递交事件
            if (this.error_allow == true){
            // 禁用掉表单的递交事件
                window.event.returnValue = false;
            }
        },
    },
})