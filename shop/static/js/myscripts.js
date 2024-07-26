$(document).ready(
    function(){
        var urlParams=new URLSearchParams(window.location.search);
        if(urlParams==""){
            localStorage.clear();
            $("#filter_state").css("display","none");
        }else{
            $("#filter_state").css("display","inline-block");
        }
        $('input:checkbox').on('click',function(){
            var fav,favs=[];
            $('input:checkbox').each(function(){
                fav={id:$(this).attre('id'),value:$(this).prop('checked')};
                favs.push(fav);
            })
            localStorage.setItem("favorites",JSON.stringify(favs));
        })
        var favorites=JSON.parse(localStorage.getItem('favorites'));
        for(var i = 0; i < favorites.length; i++){
            $('#' + favorites[i].id).prop('checked', favorites[i].value);
        }
    }
);


// -------------------------------------------------------
function showVal(x) {
    x=x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('sel_price').innerText=x;
}


// تابع حذف پارامتر های خط آدرس
function removeURLParametr(url,parametr){
    var urlparts = url.split('?');
    if (urlparts.length >= 2){
        var prefix = encodeURIComponent(parametr) + '=';
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix,0) !== -1){
                pars.splice(i,1);
            }
        }
        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}


// ------تابع انتخاب مدل مرتب سازی
function select_sort(){
    var select_sort_value = $("#select_sort").val();
    var url=removeURLParametr(window.location.href,"sort_type");
    window.location  = url + "&sort_type=" + select_sort_value;
}

// ------------------------------------------------------
status_of_shop_cart();

function status_of_shop_cart(){
    $.ajax({
        type:"GET",
        url:"/orders/status_of_shop_cart/",
        success:function(res){
            $("#indicator__value").text(res);
            // $("#indicator__value_h").text(res);
        }
    });

}

// ------------------------------------------------
function add_to_shop_cart(product_id,tedad){
    if(tedad===0){
        tedad=$("#product-quantity").val();
        alert(tedad);
    }
    $.ajax({
        type:"GET",
        url:"/orders/add_to_shop_cart/",
        data:{
            product_id: product_id,
            tedad: tedad,
        },
        success:function(res){
            status_of_shop_cart();
        }
    });

}

// -------------------------------------------------
function delete_from_shop_cart(product_id){
    $.ajax({
        type:"GET",
        url:"/orders/delete_from_shop_cart/",
        data:{
            product_id:product_id,
        },
        success:function(res){
            alert("کالای مورد نظر از سبد خرید شما حذف شد");
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}


// ---------------------------------------------
function update_shop_cart(){
    var product_id_list=[]
    var tedad_list =[]
    $("input[id^='tedad_']").each(function(index){
        product_id_list.push($(this).attr('id').slice(6))
        tedad_list.push($(this).val())
    });
    $.ajax({
        type:"GET",
        url:"/orders/update_shop_cart/",
        data:{
            product_id_list:product_id_list,
            tedad_list:tedad_list,
        },
        success:function(res){
            $("#shop_cart_list").html(res);
            status_of_shop_cart();
        }
    });
}


// --------------------------------------------------------
function showCreateCommentForm(productId,commentId,slug){
    $.ajax({
        type:"GET",
        url:"/csf/create_comment/" + slug,
        data:{
            productId:productId,
            commentId:commentId,
        },
        success:function(res){
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }

    });
}

// --------------------------------------------------------
// function UpdateAvgScore(score,productId){
//     for (let i = 1; i <= score; i++){
//         const element = document.getElementById("star_" + i);
//     }
//     $.ajax({
//         type:"GET",
//         url:"/csf/update_avg_score/",
//         data:{
//             productId: productId,
//             score: score,
//         },
//         success: function(res){
//             alert(res);
//             $("star_" + i).html(res);
//             // $("star_" + i).text(res);
//         }
//     });
// }

// ----------------------------------------------------------
function addScore(score,productId){
    var starRaiting=document.querySelectorAll(".fa-star");
    starRaiting.forEach(element => {
        element.classList.remove("checked");
    });

    for (let i = 1; i <= score; i++){
        const element = document.getElementById("star_" + i);
        element.classList.add("checked");
    }
    $.ajax({
        type: "GET",
        url:"/csf/add_score/",
        data:{
            productId: productId,
            score: score,
        },
        success: function(res){
            alert(res);
            // UpdateAvgScore(score,productId);
        }
    });
    starRaiting.forEach(element => {
        element.classList.add("disabled");
    });
}
// ------------------------------------------------------------
statuse_of_favorite_list();

function statuse_of_favorite_list(){
    $.ajax({
        type:"GET",
        url:"/csf/statuse_of_favorite_list/",
        success: function(res){
            if(Number(res) === 0){
                $('#favorite_count_icon').hide();
            } else {
                $('#favorite_count_icon').show();
                $('#favorite_count').text(res);
                // $("#indicator__value__heart").text(res);    

            }
        }
    });
}
// ----------------------------------------------------------
// function update_favorite(product_id){
//     $.ajax({
//         type:"GET",
//         url:"",
//         data:{
//             product_id:product_id,
//         },
//         success:function(res){
//             $("#").html(res);
//             statuse_of_favorite_list();
//         }
//     });
// }

// -------------------------------------------------------------
function addToFavorite(productId){
    $.ajax({
        type:"GET",
        url:"/csf/add_to_favorite/",
        data:{
            productId: productId,
        },
        success: function(res){
            alert(res)
            statuse_of_favorite_list();

        }
    });
}

// ------------------------------------------------------
function deleteFromFavorite(product_id){
    $.ajax({
        type:"GET",
        url:"/products/delete_from_favorite/",
        data:{
            product_id:product_id,
        },
        success:function(res){
            alert('حذف با موفقیت انجام شد');    
            $("#favorite_list").html(res);
            statuse_of_favorite_list();           


        }
    });
}

// ---------------------------------------------------
statuse_of_compare_list();

function statuse_of_compare_list(){
    $.ajax({
        type:"GET",
        url:"/products/statuse_of_compare_list/",
        success: function(res){
            if(Number(res) === 0){
                $('#compare_count_icon').hide();
            } else {
                $('#compare_count_icon').show();
                $('#compare_count').text(res);

            }
          
        }
    });
}

// ------------------------------------------------------
function addToCompaleList(productId,productGroupId){
    $.ajax({
        type:"GET",
        url:"/products/add_to_compare_list/",
        data:{
            productId: productId,
            productGroupId: productGroupId,
        },
        success: function(res){
            alert(res)
            statuse_of_compare_list();           
        }
    });
}

// -------------------------------------------------------
function deleteFormCompareList(productId){
    $.ajax({
        type:"GET",
        url:"/products/delete_from_compare_list/",
        data:{
            productId: productId,
        },
        success: function(res){
            alert('حذف با موفقیت انجام شد');
            $('#compare_list').html(res);
            statuse_of_compare_list();           
        }
    });
}

