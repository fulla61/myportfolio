// js/script.js

document.addEventListener('DOMContentLoaded', function () {

    // --- スムーススクロール ---
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // ページ内アンカーリンクの場合のみ処理
            if (href.length > 1 && href.startsWith('#') && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
            // ナビゲーションの場合、クリック後にモバイルメニューを閉じる処理などを追加可能
        });
    });

    // --- ナビゲーションリンクのアクティブ化 ---
    const navLinks = document.querySelectorAll('header nav ul li a');
    const currentPath = window.location.pathname.split("/").pop() || 'index.html'; // 現在のファイル名を取得

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href').split("/").pop();
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active'); // 他のリンクからactiveを削除
        }
    });

    // --- スキルバーのアニメーション (Skillsページのみ) ---
    // この関数はSkillsページが読み込まれたときに呼び出す
    function animateSkillBars() {
        const skillLevels = document.querySelectorAll('.skill-level');
        if (skillLevels.length === 0) return; // スキルバーがなければ何もしない

        skillLevels.forEach(skill => {
            const level = skill.getAttribute('data-level');
            skill.style.width = '0%'; // 初期状態
            // ビューポートに入ったらアニメーション開始 (簡易的な遅延で代替)
            setTimeout(() => {
                skill.style.width = level;
                skill.textContent = level;
            }, 200 + Math.random() * 300); // 少しランダムな遅延
        });
    }

    // skills.html の body タグに class="skills-page-body" を追加した場合の判定
    if (document.body.classList.contains('skills-page-body')) {
        animateSkillBars();
    }
    // または、URLで判定 (例: /skills.html の場合)
    if (window.location.pathname.includes('skills.html')) {
        // Intersection Observer を使って、スキルバーが画面内に入ったらアニメーションを開始するのがより良い
        const skillBarContainers = document.querySelectorAll('.skill-bar-container');
        const observerOptions = {
            root: null, // ビューポートをルートとする
            rootMargin: '0px',
            threshold: 0.3 // 30%見えたら発火
        };

        const observerCallback = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const skillLevelEl = entry.target.querySelector('.skill-level');
                    if (skillLevelEl && skillLevelEl.style.width === '0%') { // まだアニメーションしていなければ
                        const level = skillLevelEl.getAttribute('data-level');
                        skillLevelEl.style.width = level;
                        skillLevelEl.textContent = level;
                    }
                    // 一度表示したら監視を止める場合
                    // observer.unobserve(entry.target);
                }
            });
        };
        const skillObserver = new IntersectionObserver(observerCallback, observerOptions);
        skillBarContainers.forEach(container => skillObserver.observe(container));
    }


    // --- スクロールに応じたフェードインアニメーション ---
    const fadeElements = document.querySelectorAll('.fade-in-section');
    if (fadeElements.length > 0) {
        const fadeInObserverOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15 // 15%見えたら発火
        };

        const fadeInCallback = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target); // 一度表示したら監視を止める
                }
            });
        };
        const fadeInObserver = new IntersectionObserver(fadeInCallback, fadeInObserverOptions);
        fadeElements.forEach(el => fadeInObserver.observe(el));
    }

    // デバッグ用メッセージ
    console.log("Portfolio script loaded and initialized!");
});

