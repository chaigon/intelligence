exports.user = {
  //检查登陆状态，如果未登录跳转到登陆页面
  checkLogon: function(transition) {
    let token = localStorage.getItem('user_id');
    if (transition.to.auth && (!token || token === null)) { // need to auth but token is not set
      transition.redirect('/login')
    }
    transition.next()
  },
  logout: function() {
    Vue.$http.get('/api/logout/').then(function (response) {
      if (response.data.status === 200) {
        localStorage.removeItem("user_id");
        Vue.$router.go({name: "login"});
      } else {
      }
    },function(response){
      Api.user.requestFalse(response);
    })
  },
  requestFalse: function(response){
    if(response.data.return_code==201){
      window.location.href="/login"
    }else{
      console.log("在平坦的路面上曲折前行");


    }
  },
}
