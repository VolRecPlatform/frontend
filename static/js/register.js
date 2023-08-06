$(function (){
    $("#captcha-btn").click(function (event){
        var $this = $(this)
       event.preventDefault();

       var email = $("input[name='email']").val();
       $.ajax({
           url:"/auth/captcha/email?email="+email,
           method:"GET",
           success: function (result){
               var code = result['code'];
               if (code == 200){
                   var countdown = 60;
                   $this.off("click")
                   var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown -=1
                       if (countdown<=0){
                           clearInterval(timer);
                           $this.text("获取验证码");
                            bindEmailCaptchaClick();
                       }
                       },1000
                   )
                   alert("邮件验证码发送成功！")
               }else{
                   alert(result['message']);
               }
           },
           fail: function (error){
               console.log(error);
           }
       })
    });
});


    $("#tb").bootstrapTable({
        pagination: true,   //是否显示分页条
        pageSize: 3,   //一页显示的行数
        paginationLoop: false,   //是否开启分页条无限循环，最后一页时点击下一页是否转到第一页
        pageList: [5, 10, 20]   //选择每页显示多少行，数据过少时可能会没有效果
    });
