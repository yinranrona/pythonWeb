$(document)
  .ready(function(){
    $('.ui.form')
      .form({
        fields: {
          userid: {
            identifier : 'userid',
            rules: [
              {
                type   : 'empty',
                prompt : 'ユーザーIDを入力してください。'
              }
            ]
          },
          password: {
            identifier : 'password',
            rules: [
              {
                type   : 'empty',
                prompt : 'パスワードを入力してください。'
              },
              {
                type   : 'length[6]',
                prompt : '6文字数以上のパスワードを入力してください。'
              }
            ]
          }
        }
      });
  });
