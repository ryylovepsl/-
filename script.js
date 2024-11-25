// 修改 API_URL 配置，确保使用正确的协议
const API_URL = window.location.protocol === 'https:' 
    ? 'https://你的生产环境域名'
    : 'http://127.0.0.1:5000';

// 导航栏激活状态
document.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.site-header nav a');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.pageYOffset >= sectionTop - 60) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// 添加滚动动画
function handleScroll() {
    const sections = document.querySelectorAll('section');
    const triggerBottom = window.innerHeight * 0.8;

    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop < triggerBottom) {
            section.classList.add('active');
        }
    });
}

// 监听滚动事件
window.addEventListener('scroll', handleScroll);
// 初始加载时也触发一次
document.addEventListener('DOMContentLoaded', handleScroll);

// 添加证书查看功能
function showCertificate(imagePath) {
    const modal = document.getElementById('certificateModal');
    const certificateImage = document.getElementById('certificateImage');
    
    certificateImage.src = imagePath;
    modal.style.display = 'block';

    // 点击关闭按钮关闭模态框
    document.querySelector('.close-modal').onclick = function() {
        modal.style.display = 'none';
    }

    // 点击模态框外部关闭
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}