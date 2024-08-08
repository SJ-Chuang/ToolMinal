var is_mobile = /Mobi|Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
if (is_mobile) {
    document.querySelectorAll(".sizer").forEach(sizer => {
        if (sizer.hasAttribute("mobile-fs")) {
            sizer.style.fontSize = sizer.getAttribute("mobile-fs");
        }
        if (sizer.hasAttribute("mobile-width")) {
            sizer.style.width = sizer.getAttribute("mobile-width");
        }
        if (sizer.hasAttribute("mobile-height")) {
            sizer.style.height = sizer.getAttribute("mobile-height");
        }
        if (sizer.hasAttribute("mobile-mt")) {
            sizer.style.marginTop = sizer.getAttribute("mobile-mt");
        }
    })
    document.querySelectorAll(".dropdown").forEach(item => {
        item.classList.add("is-mobile");
    })
}