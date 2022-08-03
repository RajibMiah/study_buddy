

window.onload = function() {
    if (window.jQuery) {  
        // jQuery is loaded  

        $('#followers').click(function(){
           console.log('clicked')
           $('.follow-span').text('unfollow')
        })

    } else {
        // jQuery is not loaded
        alert("Doesn't Work");
    }
}

