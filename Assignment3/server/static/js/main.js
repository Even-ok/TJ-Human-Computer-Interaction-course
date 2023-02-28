const collect = []

function myFunction(){

	document.getElementById("predictedResult").innerHTML= "";
	$('#clear').hide();
	}

function getCollection(){
    	// $("#show_image_popup").fadeIn();
    for (var i=0;i<6;i++)
{ 
    var blockName = "image "+(i+1);
    if(document.getElementsByClassName(blockName)[0].style.display!="none")
    {
        var imgName = "main_img"+i;
        collect.push(document.getElementById(imgName).src);
        break;
    }
}
    for(var i=0;i<collect.length;i++){
        console.log(collect[i])
        document.getElementById("collect_img" + (i+1)).src = collect[i]
    }
}

function show_image(){
    // $("#show_image_popup").fadeIn();
    debugger;
    var selectedFile = document.getElementById('file').files[0];
    var name = selectedFile.name;//读取选中文件的文件名
    var path = "../static/uploads/"
    console.log("文件名:"+name, "路径:" +path+name )
    document.getElementById("large-image").src = path+name;
    $("#show_image_popup").show()
}

function close_img(){
    $("#show_image_popup")[0].style.display="none"
}

//我们得到文件后缀名后，根据后缀即可判断文件的类型（文件格式）。比如我们需要判断一个文件是否是图片格式，首先定义一个判断函数：
function isAssetTypeAnImage(ext) {
    return [
    'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff'].
    indexOf(ext.toLowerCase()) !== -1;
   }
   
function changeColor(){
    var heart = document.getElementById("love");
    heart.style.background = "#e82626db";
}

function typeSelect(){
debugger;
 var value = $('#typechange')[0].value;
 //alert(value);
 var satisfy_url = [];
for(var i=0;i<6;i++){

    var caption = document.getElementById("sidebar-name"+ (i+1)).innerText;
    if (caption != value)
    {
        //document.getElementById("sidebar-name" + (i+1)).value = None;
        var imgName = "img"+i;
        //document.getElementById("sidebar-name" + (i+1)).src = "../static/image/gray.jpg"
    }
    else{
        var imgName = "img"+i;
        satisfy_url.push(document.getElementById(imgName).src);
    }
    var imgName = "img"+i;
    //先置为灰色，None
    document.getElementById(imgName).src = "static/image/gray.jpg";
    document.getElementById("sidebar-name" + (i+1)).innerText = "None";
}

for(var i=0;i<satisfy_url.length;i++){
    document.getElementById("sidebar-name"+ (i+1)).innerText = value;
    var imgName = "img"+i;
    document.getElementById(imgName).src = satisfy_url[i];

}

}


function fun(){

    var selectedFile = document.getElementById('file').files[0];
    var name = selectedFile.name;//读取选中文件的文件名

    //获取最后一个.的位置
    var index= name.lastIndexOf(".");
    //获取后缀
    var ext = name.substr(index+1);
    //判断是否是图片
    console.log("该文件是否为图片：" + isAssetTypeAnImage(ext));
    
    if(!isAssetTypeAnImage(ext)){
        alert("Please input image!");
        return false;
    }

    $('#load').show();
    $("form").submit(function(evt){	 
    //$('#loader-icon').show(); 
                    
    evt.preventDefault();
    
            //$('#loader-icon').show();
        var formData = new FormData($(this)[0]);
        
    $.ajax({
            url: 'imgUpload',
            type: 'POST',
            data: formData,
            //async: false,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
    
            success: function (response) {
        $('#load').hide();
        $('#row1').show();
        //$('#clear').show();
                //console.log(response[1]);
            //document.getElementById("predictedResult").innerHTML= response; 

                document.getElementById("img0").src = response.image0;
                document.getElementById("img1").src = response.image1;
                document.getElementById("img2").src = response.image2;
                document.getElementById("img3").src = response.image3;
                document.getElementById("img4").src = response.image4;
                document.getElementById("img5").src = response.image5;

                document.getElementById("main_img0").src = response.image0;
                document.getElementById("main_img1").src = response.image1;
                document.getElementById("main_img2").src = response.image2;
                document.getElementById("main_img3").src = response.image3;
                document.getElementById("main_img4").src = response.image4;
                document.getElementById("main_img5").src = response.image5;

                document.getElementById("sidebar-name1").innerHTML = response.image0_type;
                document.getElementById("sidebar-name2").innerHTML = response.image1_type;
                document.getElementById("sidebar-name3").innerHTML = response.image2_type;
                document.getElementById("sidebar-name4").innerHTML = response.image3_type;
                document.getElementById("sidebar-name5").innerHTML = response.image4_type;
                document.getElementById("sidebar-name6").innerHTML = response.image5_type;
                // document.getElementById("img6").src = response.image6;
                // document.getElementById("img7").src = response.image7;
                // document.getElementById("img8").src = response.image8;
        //         $('#table').show();
        // $('#clear').show();
            
            }
    });
    
return false;
 })};

 function reset(){

    // 删除上传的图片
    
    var file = document.getElementById('file');
    
    file.value = '';
    
    }

function toCamera(){

    window.location.href="camera";

}