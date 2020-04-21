let vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: getCookie('username'),
        is_show_edit: false,
        form_databases: {
            // title: '',
            host_ip: '',
            dbuser: '',
            dbpassword: '',
            dbport: '',
            // mobile: '',
            // tel: '',
            // email: '',
        },
        userdatabases: JSON.parse(JSON.stringify(userdatabases)),

        editing_database_index: '',
        edit_title_index: '',
        new_title: '',

        error_host_ip: false,
        error_dbuser: false,
        error_dbpassword: false,
        error_dbport: false,

    },


    methods: {
        // 展示新增用户数据库弹框
        show_add_site(){
            this.is_show_edit = true;
            // 清空错误提示信息
            this.clear_all_errors();
            // 清空原有数据
            this.form_databases.host_ip = '';
            this.form_databases.dbuser = '';
            this.form_databases.dbpassword = '';
            this.form_databases.dbport = '';
            this.editing_database_index = '';
        },
        // 展示编辑地址弹框
        show_edit_site(index){
            this.is_show_edit = true;
            this.clear_all_errors();
            this.editing_database_index = index.toString();
            // 只获取要编辑的数据
            this.form_databases = JSON.parse(JSON.stringify(this.userdatabases[index]));
        },
        // 校验服务器IP
        check_host_ip(){
            if (!this.form_databases.host_ip) {
                this.error_host_ip = true;
            } else {
                this.error_host_ip = false;
            }
        },
        // 校验数据库用户
        check_dbuser(){
            if (!this.form_databases.dbuser) {
                this.error_dbuser = true;
            } else {
                this.error_dbuser = false;
            }
        },
        // 校验数据库密码
        // check_mobile(){
        //     let re = /^1[3-9]\d{9}$/;
        //     if(re.test(this.form_address.mobile)) {
        //         this.error_mobile = false;
        //     } else {
        //         this.error_mobile = true;
        //     }
        // },
        // 校验数据库密码
        check_dbpassword(){
            if (!this.form_databases.dbpassword) {
                this.error_dbpassword = true;
            } else {
                this.error_dbpassword = false;
            }
        },
        // 校验数据库端口
        check_dbport(){
            if (!this.form_databases.dbport) {
                this.error_dbport = true;
            } else {
                this.error_dbport = false;
            }
        },

        // 清空错误提示信息
        clear_all_errors(){
            this.error_host_ip = false;
            this.error_dbuser = false;
            this.error_dbpassword = false;
            this.error_dbport = false;

        },

        // 新增用户数据库
        save_database(){
            if (this.error_host_ip || this.error_dbuser || this.error_dbpassword || this.error_dbport) {
                alert('信息填写有误！');
            } else {
                // 注意：0 == '';返回true; 0 === '';返回false;
                if (this.editing_database_index === '') {
                    // 新增用户数据库
                    let url = '/databases/create/';
                    axios.post(url, this.form_databases, {
                        headers: {
                            'X-CSRFToken':getCookie('csrftoken')
                        },
                        responseType: 'json'
                    })
                        .then(response => {
                            if (response.data.code == '0') {
                                // 局部刷新界面：展示所有地址信息，将新的地址添加到头部
                                this.userdatabases.splice(0, 0, response.data.database);
                                this.is_show_edit = false;
                            } else if (response.data.code == '4101') {
                                location.href = '/login/?next=/databases/';
                            } else {
                                alert(response.data.errmsg);
                            }
                        })
                        .catch(error => {
                            console.log(error.response);
                        })
                } else {
                    // 修改地址
                    let url = '/databases/' + this.userdatabases[this.editing_database_index].id + '/';
                    axios.put(url, this.form_databases, {
                        headers: {
                            'X-CSRFToken':getCookie('csrftoken')
                        },
                        responseType: 'json'
                    })
                        .then(response => {
                            if (response.data.code == '0') {
                                this.userdatabases[this.editing_database_index] = response.data.database;
                                this.is_show_edit = false;
                            } else if (response.data.code == '4101') {
                                location.href = '/login/?next=/databases/';
                            } else {
                                alert(response.data.errmsg);
                            }
                        })
                        .catch(error => {
                            alert(error.response);
                        })
                }
            }
        },
        // 删除用户数据库
        delete_database(index){
            let url = '/databases/' + this.userdatabases[index].id + '/';
            axios.delete(url, {
                headers: {
                    'X-CSRFToken':getCookie('csrftoken')
                },
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.code == '0') {
                        // 删除对应的标签
                        this.userdatabases.splice(index, 1);
                    } else if (response.data.code == '4101') {
                        location.href = '/login/?next=/databases/';
                    }else {
                        alert(response.data.errmsg);
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        },

        // 展示数据库title编辑框
        show_edit_title(index){
            this.edit_title_index = index;
        },
        // 取消保存数据库title
        cancel_title(){
            this.edit_title_index = '';
            this.new_title = '';
        },
        // 修改用户数据库title
        save_title(index){
            if (!this.new_title) {
                alert("请填写标题后再保存！");
            } else {
                let url = '/databases/' + this.userdatabases[index].id + '/title/';
                axios.put(url, {
                    title: this.new_title
                }, {
                    headers: {
                        'X-CSRFToken':getCookie('csrftoken')
                    },
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.code == '0') {
                            // 更新地址title
                            this.userdatabases[index].title = this.new_title;
                            this.cancel_title();
                        } else if (response.data.code == '4101') {
                            location.href = '/login/?next=/databases/';
                        } else {
                            alert(response.data.errmsg);
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
    }
});