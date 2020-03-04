$(function(){
    $('#get-more').click(function(){
        $.ajax({
            type:'get',
            url:"http://127.0.0.1:5000/get_item/all",
            success:function(data){
                var item_data = JSON.stringify(data);
                var obj = JSON.parse(item_data);
                var items = JSON.stringify(obj["data"]);
                items = items.replace('[','');
                items = items.replace(']','');
                var list = items.split('}');
                console.log(list);
                $.each(list,function(k,v){
                    var sub = v.replace('{','');
                    sub = sub.replace(':','');
                    if(sub != ""){
                        var sub_list = sub.split(',');
                        $.each(sub_list,function(sk,sv){
                            $('#target').append("<p>:"+sv+"</p>");
                        })
                        }
                });

            },
        });
    })
})