const fps = 60;

video.addEventListener('play', function(){
    sendFrame(this)
})


function sendFrame(video){
    var type = "image/png";
    setInterval(() => {
        
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        const data = canvas.toDataURL(type,0.001);
        socket.emit('image', data);
        
    }, 10000/fps);
}


socket.on('response_back', function(image){
    image_id.src = image;
});
            