// ************************* url *************************
var url = 'main.php';

// 페이지 로드 시에 DB 가져오기
window.onload = function(){
    fetchDB();
}

// DB 가져오기
function fetchDB(){
    $.ajax({
        url: url,
        type: 'GET',
    // ************************* JSON parsing해서 뿌려주기!
        success: function(uid, name, tel, coupon){
            $('.table').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody></tbody></table>');
            $('.table > .table_list > tbody:last').append('<tr><td class="id">'+uid+'</td><td class="name">'+name+'</td><td class="phone">'+tel+'</td><td class="coupon">'+coupon+'</td></tr>');
        },
        error: function(data){
            $('alert').append('<p>데이터베이스를 가져오는 에 실패했습니다. 다시 시도해주세요.</p>');
        }
    });
}

// DB 실험용(DB대신 text 읽어오기) -> 실패ㅠㅠ
function fetchDB2(){
    var fileName = 'file:///Users/genevie/Desktop/Project/Embadded/FingerStamp/test.txt';
    var reader = new FileReader();
    
    
    reader.onload = function(event){
        Clear();
        $('.table').empty();
        console.log(event.target.result);
        reader.readAsText(fileName);
    }
    reader.onerror = function(){
        Clear();
        $('.alert').append('<p>파일을 열 수 없습니다.</p>');
    }
}

// DB에 있는 지 확인
function isExist(uid, name, phone, coupon){
    // ********************* DB ***********************
    return true;
}

// 초기화
function Clear(){
    $('.alert').empty();
    $('form').each(function(){
        this.reset();
    });
    $('.userInfo').empty();
}

// info 초기화
$('#clear').click(function(){
    Clear();
});

// 새 고객이면 인식 후 DB에 추가되고 사용자 정보 띄워줌
// 기존 고객이면 인식 후 사용자 정보 띄워줌
$('#userAuth').click(function(){
    $('.alert').empty();
    //$('.alert').append('<p>지문을 인식해주세요.</p>');

    var name = $('#name_input').val();
    var phone = $('#phone_input').val();
    var coupon = $('#coupon_input').val();
    if(coupon == "")
        $('.alert').append('<p>쿠폰 개수를 입력해주세요.</p>');
    else{
        $.ajax({
            url: url,
            type: 'GET',
            data: {
                phone: phone,
                name : name,
                stamp: coupon
            },
            success: function(type, uid, name, tel, coupon){
                $('.alert').empty();

                if(type == 'register'){
                    $('.alert').append('<p>사용자가 추가되었습니다.</p>');
                    fetchDB();
                }
                else
                    $('.alert').append('<p>사용자가 인식되었습니다.</p>');
                
                //Clear();
                $('.userInfo').empty();
                $('.userInfo').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody><tr><td class="id">'+uid+'</td><td class="name">'+name+'</td><td class="phone">'+tel+'</td><td class="coupon">'+coupon+'</td></tr></tbody></table>');
                plus = 0;
                minus = 0;
            },
            error: function(data){
                $('.alert').append('<p>사용자 인식에 실패했습니다. 다시 시도해주세요.</p>');
    // **** 확인용 *****
                //Clear();
                $('.userInfo').empty();
                $('.userInfo').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody><tr><td class="id">uid</td><td class="name">'+name+'</td><td class="phone">'+phone+'</td><td class="coupon">'+coupon+'</td></tr></tbody></table>');
                plus = 0;
                minus = 0;
    // ***************            
            }
        });   
    }   
});

// 지문 인식 후에 삭제 가능하다고 가정함
$('#userDel').click(function(){
    $('.alert').empty();

    $.ajax({
        url: url,
        type: 'GET',
        success: function(data){
            $('.alert').append('<p>사용자가 삭제되었습니다.</p>');
            $('.table').empty();
            fetchDB();
        },
        error:function(data){
        	$('.alert').append('<p>사용자 삭제에 실패했습니다. 다시 시도해주세요.</p>');
    // **** 확인용 ****
            //$('.table').empty();
            fetchDB();
    // ***************
        }
    });
});

// 지문 인식 후에 사용 가능하다고 가정함
// 리스트에서 id를 기준으로 coupon 개수 가져와서 입력한 coupon 개수 뺌
$('#coupUse').click(function(){
    $('.alert').empty();
    
    var uid = $('#id_input').val();
    var name = $('#name_input').val();
    var phone = $('#phone_input').val();
    var coupon = $('.table tr:nth-child('+uid+') td:nth-child(4)').text();
    var coupon2 = $('#coupon_input').val();
    
    if(isExist(uid, name, phone, coupon)){
        $.ajax({
            url: url,
            type: 'GET',
            data: {
                uid: uid,
                number : coupon
            },
            success: function(coupon){
                $('.alert').append('<p>쿠폰을 사용하였습니다.</p>');
                //Clear();
                $('.userInfo').empty();
                $('.userInfo').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody><tr><td class="id">'+uid+'</td><td class="name">'+name+'</td><td class="phone">'+tel+'</td><td class="coupon">'+(coupon-coupon2)+'</td></tr></tbody></table>');
                plus = 0;
                minus = 0;
                fetchDB();
            },
            error:function(data){
                $('.alert').append('<p>쿠폰 사용에 실패했습니다. 다시 시도해주세요.</p>');
         // **** 확인용 *****
                //Clear();
                $('.userInfo').empty();
                $('.userInfo').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody><tr><td class="id">uid</td><td class="name">'+name+'</td><td class="phone">'+phone+'</td><td class="coupon">'+(coupon-coupon2)+'</td></tr></tbody></table>');
                plus = 0;
                minus = 0;
                fetchDB();
        // ***************    
            }
        });
    }
    else{
        Clear();
        $('.alert').append('<p>올바른 사용자가 아닙니다. 다시 시도해주세요.</p>');
    }
});

var plus = 0, minus = 0;
// + 버튼 누른 개수
$('.plus').click(function(){
    var coupon = $('#coupon_input').val();
    $('#coupon_input').val(coupon*1+1);
    plus++;
});
// - 버튼 누른 개수
$('.minus').click(function(){
    var coupon = $('#coupon_input').val();
    $('#coupon_input').val(coupon*1-1);
    minus++;
});

// 지문 인식 후에 수정 가능하다고 가정함
$('#coupModi').click(function(){
    $('.alert').empty();

    var uid = $('#id_input').val();
    var name = $('#name_input').val();
    var phone = $('#phone_input').val();
    var coupon = $('#coupon_input').val();
    console.log(plus+', '+minus);
    if(isExist(uid, name, phone, coupon)){
        $.ajax({
            url: url,
            type: 'GET',
            data: {
                uid: uid,
                add: plus,
                sub: minus 
            },
            success: function(type, uid, name, tel, coupon){
                $('.alert').append('<p>쿠폰을 수정하였습니다.</p>');
                $('.userInfo').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody><tr><td class="id">'+uid+'</td><td class="name">'+name+'</td><td class="phone">'+tel+'</td><td class="coupon">'+coupon+'</td></tr></tbody></table>');
                plus = 0;
                minus = 0;
            },
            error:function(data){
                $('.alert').append('<p>쿠폰 수정에 실패했습니다. 다시 시도해주세요.</p>');
        // **** 확인용 *****
                //Clear();
                $('.userInfo').empty();
                $('.userInfo').append('<table class="table_list" cellspacing="0"><thead><th width="10%">Id</th><th width="40%">Name</th><th width="40%">Phone</th><th width="10%">Coupon</th></tr></thead><tbody><tr><td class="id">uid</td><td class="name">'+name+'</td><td class="phone">'+phone+'</td><td class="coupon">'+coupon+'</td></tr></tbody></table>');
                plus = 0;
                minus = 0;
                //fetchDB();
        // *************** 
            }
        });
    }
    else{
        Clear();
        $('.alert').append('<p>올바른 사용자가 아닙니다. 다시 시도해주세요.</p>');
    }
});