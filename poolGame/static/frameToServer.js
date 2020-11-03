const fps = 70;

video.addEventListener('play', function(){
    sendFrame()
})

function sendFrame(){
    var video = document.getElementById("videoElement");
    var type = "image/png";
    setInterval(() => {
        
        var frame = capture(video, 1);
        var data = frame.toDataURL(type,0.8);
        //data = data.replace('data:' + type + ';base64,', '');
        socket.emit('image', data);
        data.delete();
    }, 10000/fps);
}


socket.on('response_back', function(image){
    image_id.src = image;
});
            