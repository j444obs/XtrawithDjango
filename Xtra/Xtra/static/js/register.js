// 采用ES6语法
// 创建Vue对象vm
let vm = new Vue({
    el: '#app',     // 通过ID选择器找到绑定的HTML内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data:{      // 数据对象
        // v-model
        username:'',
        password:'',
        password2:'',
        allow:'',
        image_code_url: '',
        uuid: '',
        image_code: '',

        // v-show
        error_name:false,
        error_password:false,
        error_password2:false,
        error_allow:false,
        error_image_code:false,

        // error_message
        error_name_message:'',
        error_image_code_message:'',
    },
    mounted(){  // 页面加载完会被调用的
        // 生成图形验证码
        this.generate_image_code();
    },

    methods:{  // 定义和实现事件方法
        // 生成图形验证码的方法：封装的思想，代码复用
        generate_image_code(){
            this.uuid = generateUUID();
            this.image_code_url = '/image_codes/' + this.uuid + '/';
        },

        // 校验用户名
        check_username(){
        // 用户名是5-20个字符，[a-zA-Z0-9_-]
        // 定义正则
            let re = /^[a-zA-Z0-9_-]{5,20}$/
        // 使用正则匹配用户名数据
        // this当前vue对象
            if (re.test(this.username)){
            // 匹配成功，不展示错误提示信息
                this.error_name = false;
            } else {
            // 匹配失败，展示错误提示信息
                this.error_name_message = 'Please enter a username of 5-10 characters';
                this.error_name = true;
            }

            // 判断用户名重复注册
            if (this.error_name == false){      // 只有当用户输入的用户名满足条件时才会去判断
                let url = '/usernames/' + this.username + '/count';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if(response.data.count == 1){
                            // 用户名已存在
                            this.error_name_message = 'Username already exists';
                            this.error_name = true;
                        } else {
                            // 用户名不存在
                            this.error_name = false;
                        }

                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }

        },
        // 校验密码
        check_password(){
            let re = /^[0-9A-Za-z]{8,20}$/
            if (re.test(this.password)){
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 校验确认密码
        check_password2(){
            if (this.password != this.password2){
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },

        check_image_code2(){
            this.check_image_code();

            let url = '/check_image_codes/' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType: 'json',
            })
                .then(response => {
                        if (response.data.code == '4001'){      // 图形验证码错误
                            this.error_image_code_message = response.data.errmsg;
                            this.error_image_code = true;
                        }
                        else{
                            this.error_image_code = false;
                        }
                    }).catch(error => {
                    console.log(error.response);
                })
        },


        // 校验图形验证码
        check_image_code(){
            if (this.image_code.length != 4) {
                this.error_image_code_message = 'Please enter the graphic verification code';
                this.error_image_code = true;
            } else {
                this.error_image_code = false;
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

            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_image_code();
            this.check_image_code2();
            this.check_allow();
            // 在校验之后，注册数据中，只要有错误，就禁用掉表单的递交事件
            if (this.error_name == true || this.error_password == true || this.error_password2 == true
             || this.error_image_code == true || this.error_allow == true){
            // 禁用掉表单的递交事件
                window.event.returnValue = false;
            }
        },
    },
})