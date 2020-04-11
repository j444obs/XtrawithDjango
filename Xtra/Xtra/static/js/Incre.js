// 采用ES6语法
// 创建Vue对象vm
let vm = new Vue({
    el: '#app',     // 通过ID选择器找到绑定的HTML内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data:{      // 数据对象
        // v-model
        username:'',
        HostIP:'',
        password:'',
        port:'',
        filename:'',
        allow:'',

        // v-show
        error_name:false,
        error_password:false,
        error_allow:false,
        error_ip:false,
        error_port:false,
        error_filename:false,

        // error_message
        error_name_message:'',
        error_image_code_message:'',
    },

    methods:{  // 定义和实现事件方法
        // 校验IP
        check_HostIP(){
            let re = /^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$/
            if (re.test(this.HostIP)){
                this.error_ip = false;
            } else {
                this.error_ip = true;
            }
        },


        // 校验DB用户名
        check_username(){
            if(this.username == ''){
                this.error_name = true;
            }
            else {
                this.error_name = false;
            }
        },

        // 校验DB密码
        check_password(){
            if(this.password == ''){
                this.error_password = true;
            }
            else {
                this.error_password = false;
            }
        },

        // 校验DB端口
        check_port(){
            let re = /^\d{1,5}$/
            if (re.test(this.port)){
                this.error_port = false;
            } else {
                this.error_port = true;
            }
        },

        // 校验base file
        check_file(){
            //2020-04-11_02-25-44
            let re = /^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$/
            if (re.test(this.filename)) {
                this.error_filename = false;
            } else {
                this.error_filename = true;
            }
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
            this.check_HostIP();
            this.check_username();
            this.check_password();
            this.check_port();
            this.check_allow();
            this.check_file();
            // 在校验之后，注册数据中，只要有错误，就禁用掉表单的递交事件
            if (this.error_ip == true || this.error_name == true || this.error_password == true
             || this.error_port == true || this.error_allow == true || this.error_filename == true){
            // 禁用掉表单的递交事件
                window.event.returnValue = false;
            }
        },
    },
})