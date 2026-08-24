document.addEventListener("DOMContentLoaded", () => {

    const themeToggle = document.querySelector(".theme-toggle");
    const contactForm = document.querySelector("#contact-form");

    contactForm?.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(contactForm);
        const name = String(formData.get("name") || "").trim();
        const email = String(formData.get("email") || "").trim();
        const message = String(formData.get("message") || "").trim();
        const status = contactForm.querySelector(".form-status");

        if (!name || !email || !message) {
            if (status) status.textContent = "Please complete all fields.";
            return;
        }

        const subject = encodeURIComponent(`Portfolio enquiry from ${name}`);
        const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\nProject details:\n${message}`);

        if (status) status.textContent = "Opening your email app...";
        window.location.href = `mailto:111abhishek.04367@gmail.com?subject=${subject}&body=${body}`;
    });

    const projectButtons = document.querySelectorAll(".more-project-button");
    const moreProjectsToggle = document.querySelector(".more-projects-toggle");
    const moreProjectsContent = document.querySelector("#more-projects-content");
    const projectsModal = document.querySelector(".projects-modal");
    const modalClose = document.querySelector(".modal-close");
    const modalProjectImage = document.querySelector("#modal-project-image");
    const modalProjectLabel = document.querySelector("#modal-project-label");
    const modalProjectName = document.querySelector("#modal-project-name");
    const modalProjectTitle = document.querySelector("#modal-project-title");
    const modalProjectStack = document.querySelector("#modal-project-stack");
    const modalProjectDescription = document.querySelector("#modal-project-description");
    const modalProjectFeatures = document.querySelector("#modal-project-features");
    const modalProjectLink = document.querySelector("#modal-project-link");
    let lastProjectButton = null;

    const projects = {
        "hometown-hub": { label: "05 / Next.js · TypeScript", name: "Hometown Hub", title: "Community & Local Information Platform", image: "assets/lahan01.png", description: "A modern community-focused web platform designed to bring local information, services, and experiences together through a clean and responsive interface.", features: ["Community", "Local information", "Responsive UI", "TypeScript", "Next.js"], link: "https://github.com/1abhishek0948/Hometown-HUb" },
        "digital-neuro": { label: "06 / Python · AI/ML · Web Technologies", name: "Digital Neuro", title: "AI & Intelligent Digital Interaction", image: "assets/digital-neuro.png", description: "An AI-focused experimental project exploring intelligent digital interaction and machine-learning concepts through a web-based experience.", features: ["AI/ML", "Python", "Intelligent interaction", "Web technologies", "Experimentation"], link: "https://github.com/1abhishek0948" },
        "universal-media-downloader": { label: "07 / Python · Flask · yt-dlp · Bootstrap", name: "Universal Media Downloader", title: "Web-Based Media Downloader", image: "assets/umd_hero.png", description: "A Flask-powered web application for downloading supported online videos and playlists through a simple, responsive interface.", features: ["Flask", "Python", "yt-dlp", "Video downloads", "Playlist support"], link: "https://github.com/1abhishek0948/Universal-Media-downloader" },
        "blind-assistance-system": { label: "08 / Python · OpenCV · Raspberry Pi", name: "Blind Assistance System", title: "Real-Time Assistive Computer Vision System", image: "assets/blind-assist.png", description: "An assistive technology project designed to help visually impaired users understand their surroundings using computer vision, object detection, distance sensing, and voice feedback.", features: ["Object detection", "Distance detection", "OpenCV", "Voice alerts", "Raspberry Pi"], link: "https://github.com/1abhishek0948/BLIND-ASSISTANCE-SYSTEM" },
        taleforge: { label: "09 / React · Django REST · PostgreSQL · OpenAI", name: "TaleForge", title: "Interactive Story Creation Platform", image: "assets/small-project.png", description: "An interactive storytelling application focused on creating dynamic narratives and branching story experiences with AI-powered storytelling capabilities.", features: ["Story creation", "Interactive narratives", "AI", "React", "PostgreSQL", "JWT"], link: "https://github.com/1abhishek0948/TaleForge-interactive-storytelling" }
    };

    moreProjectsToggle?.addEventListener("click", () => {
        const isExpanded = moreProjectsToggle.getAttribute("aria-expanded") === "true";
        moreProjectsToggle.setAttribute("aria-expanded", String(!isExpanded));
        moreProjectsToggle.querySelector("span").textContent = isExpanded ? "More Projects" : "Hide Projects";
        moreProjectsToggle.querySelector("i").className = `fa-solid ${isExpanded ? "fa-plus" : "fa-minus"}`;
        if (moreProjectsContent) moreProjectsContent.hidden = isExpanded;
    });

    if (projectsModal && typeof projectsModal.showModal === "function") {
        projectButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const project = projects[button.dataset.project];
                if (!project) return;
                modalProjectImage.src = project.image;
                modalProjectImage.alt = `${project.name} project interface`;
                modalProjectLabel.textContent = project.label;
                modalProjectStack.textContent = project.label.split(" / ")[1];
                modalProjectName.textContent = project.name;
                modalProjectTitle.textContent = project.title;
                modalProjectDescription.textContent = project.description;
                modalProjectFeatures.replaceChildren(...project.features.map((feature) => {
                    const featureElement = document.createElement("span");
                    featureElement.textContent = feature;
                    return featureElement;
                }));
                modalProjectLink.href = project.link;
                lastProjectButton = button;
                projectsModal.showModal();
            });
        });
        const closeProjectModal = () => {
            projectsModal.close();
        };
        modalClose?.addEventListener("click", closeProjectModal);
        projectsModal.addEventListener("close", () => lastProjectButton?.focus());
        projectsModal.addEventListener("click", (event) => {
            if (event.target === projectsModal) closeProjectModal();
        });
    }

    let savedTheme = null;

    try {
        savedTheme = window.localStorage.getItem("portfolio-theme");
    } catch (error) {
        savedTheme = null;
    }

    const setTheme = (theme) => {
        const isDark = theme === "dark";

        document.documentElement.dataset.theme = isDark ? "dark" : "light";
        document.querySelector('meta[name="theme-color"]')?.setAttribute("content", isDark ? "#16171c" : "#f5f5f2");

        if (themeToggle) {
            themeToggle.setAttribute("aria-pressed", String(isDark));
            themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
            themeToggle.innerHTML = `<i class="fa-solid ${isDark ? "fa-sun" : "fa-moon"}" aria-hidden="true"></i>`;
        }
    };

    setTheme(savedTheme === "dark" ? "dark" : "light");

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
            try {
                window.localStorage.setItem("portfolio-theme", nextTheme);
            } catch (error) {
                // Private browsing can deny storage access; the toggle still works for this session.
            }
            setTheme(nextTheme);
        });
    }

    const deviceTime = document.querySelector("#device-time");
    const connectionStatus = document.querySelector("#connection-status");
    const batteryStatus = document.querySelector("#battery-status");

    const updateDeviceTime = () => {
        if (deviceTime) {
            deviceTime.textContent = new Intl.DateTimeFormat([], {
                hour: "numeric",
                minute: "2-digit"
            }).format(new Date());
        }
    };

    const updateConnectionStatus = () => {
        if (!connectionStatus) {
            return;
        }

        const isOnline = navigator.onLine;
        connectionStatus.classList.toggle("fa-wifi", isOnline);
        connectionStatus.classList.toggle("fa-wifi-slash", !isOnline);
        connectionStatus.title = isOnline ? "Online" : "Offline";
    };

    const updateBatteryStatus = (battery) => {
        if (!batteryStatus) {
            return;
        }

        const level = Math.round(battery.level * 100);
        const icon = level <= 10 ? "fa-battery-empty" :
            level <= 25 ? "fa-battery-quarter" :
                level <= 50 ? "fa-battery-half" :
                    level <= 75 ? "fa-battery-three-quarters" : "fa-battery-full";

        batteryStatus.className = `fa-solid ${icon}`;
        batteryStatus.title = `${level}%${battery.charging ? ", charging" : ""}`;
    };

    updateDeviceTime();
    updateConnectionStatus();
    window.setInterval(updateDeviceTime, 30000);
    window.addEventListener("online", updateConnectionStatus);
    window.addEventListener("offline", updateConnectionStatus);

    if (typeof navigator.getBattery === "function") {
        navigator.getBattery().then((battery) => {
            updateBatteryStatus(battery);
            battery.addEventListener("levelchange", () => updateBatteryStatus(battery));
            battery.addEventListener("chargingchange", () => updateBatteryStatus(battery));
        }).catch(() => {
            // Battery information is optional and unavailable in several browsers.
        });
    }

    const marqueeTrack = document.querySelector(".marquee-track");

    if (marqueeTrack) {
        let marqueeOffset = 0;
        let lastScrollY = window.scrollY;
        let marqueeWidth = 0;
        let framePending = false;

        const measureMarquee = () => {
            marqueeWidth = marqueeTrack.scrollWidth / 4;
        };

        const updateMarquee = () => {
            const currentScrollY = window.scrollY;
            const scrollDelta = currentScrollY - lastScrollY;

            marqueeOffset -= scrollDelta * 0.7;

            if (marqueeWidth > 0) {
                marqueeOffset %= marqueeWidth;
            }

            marqueeTrack.style.transform = `translate3d(${marqueeOffset}px, 0, 0)`;
            lastScrollY = currentScrollY;
            framePending = false;
        };

        const handleScroll = () => {
            if (!framePending) {
                window.requestAnimationFrame(updateMarquee);
                framePending = true;
            }
        };

        measureMarquee();
        window.addEventListener("resize", measureMarquee);
        window.addEventListener("scroll", handleScroll, { passive: true });
    }

    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach((item) => {

        item.addEventListener("click", () => {

            const targetId = item.dataset.target;

            const target = document.getElementById(targetId);

            if (!target) {
                return;
            }

            // Remove active state
            navItems.forEach((nav) => {
                nav.classList.remove("active");
                nav.removeAttribute("aria-current");
            });

            // Activate clicked button
            item.classList.add("active");
            item.setAttribute("aria-current", "page");

            // Smooth scroll
            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });


    // Update active navigation while scrolling
    const sections = document.querySelectorAll(
        "#home, #about, #capabilities, #experience, #projects, #contact"
    );

    if (typeof IntersectionObserver !== "undefined") {
        const observer = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    const sectionId = entry.target.id;

                    const navTarget = sectionId === "capabilities" || sectionId === "experience"
                        ? "capabilities"
                        : sectionId;

                    navItems.forEach((item) => {

                        if (item.dataset.target === navTarget) {

                            navItems.forEach((nav) => {
                                nav.classList.remove("active");
                                nav.removeAttribute("aria-current");
                            });

                            item.classList.add("active");
                            item.setAttribute("aria-current", "page");
                        }

                    });

                }

            });

        },
        {
            root: null,
            rootMargin: "-20% 0px -55%",
            threshold: 0
        }
        );

        sections.forEach((section) => {
            observer.observe(section);
        });
    }


    // CV button feedback
    const cvButton = document.querySelector(".cv-button");

    if (cvButton) {

        cvButton.addEventListener("click", () => {

            cvButton.style.transform = "scale(0.95)";

            setTimeout(() => {
                cvButton.style.transform = "";
            }, 150);

        });

    }


    // Social link hover/click animation
    const socialLinks = document.querySelectorAll(".social-links a");

    socialLinks.forEach((link) => {

        link.addEventListener("click", () => {

            link.style.transform = "scale(0.9)";

            setTimeout(() => {
                link.style.transform = "";
            }, 150);

        });

    });

});
