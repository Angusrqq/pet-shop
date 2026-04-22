class ProductSlider {
    constructor(sliderContainer, itemsPerPage = 5) {
        this.container = sliderContainer;
        this.track = this.container.querySelector('.slider-track');
        this.prevBtn = this.container.querySelector('.prev-btn');
        this.nextBtn = this.container.querySelector('.next-btn');
        this.itemsPerPage = itemsPerPage;
        this.currentPage = 0;
        this.items = Array.from(this.track.children);
        this.totalItems = this.items.length;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);

        this.isUpdating = false;
        this.resizeTimeout = null;
        
        this.init();
    }
    
    init() {
        if (this.totalItems === 0) return;
        
        this.track.style.display = 'flex';
        this.track.style.transition = 'transform 0.3s ease-in-out';
        
        this.updateButtons();
        this.attachEvents();
        this.updateVisibleItems();
        
        window.addEventListener('resize', () => this.handleResize());
    }
    
    getItemWidth() {
        const firstItem = this.items[0];
        if (!firstItem) return 0;
        
        const styles = window.getComputedStyle(firstItem);
        const width = firstItem.offsetWidth;
        const marginRight = parseFloat(styles.marginRight) || 0;
        const marginLeft = parseFloat(styles.marginLeft) || 0;
        
        const trackStyles = window.getComputedStyle(this.track);
        const gap = parseFloat(trackStyles.gap) || 20;
        
        return width + marginRight + marginLeft + gap;
    }
    
    updateVisibleItems() {
        if (this.isUpdating) return;
        this.isUpdating = true;
        
        let newItemsPerPage = this.getItemsPerPageByScreenWidth();
        
        if (newItemsPerPage !== this.itemsPerPage) {
            this.itemsPerPage = newItemsPerPage;
            this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
            
            if (this.currentPage >= this.totalPages) {
                this.currentPage = Math.max(0, this.totalPages - 1);
            }
        }
        
        this.updateSliderPosition();
        this.updateButtons();
        
        this.isUpdating = false;
    }
    
    getItemsPerPageByScreenWidth() {
        const width = window.innerWidth;
        if (width <= 576) return 1;
        if (width <= 768) return 2;
        if (width <= 992) return 3;
        if (width <= 1200) return 4;
        return this.itemsPerPage;
    }
    
    updateSliderPosition() {
        if (this.totalItems === 0) return;
        
        const itemWidth = this.getItemWidth();
        const scrollAmount = this.currentPage * (itemWidth * this.itemsPerPage);
        this.track.style.transform = `translateX(-${scrollAmount}px)`;
    }
    
    updateButtons() {
        if (this.prevBtn && this.nextBtn) {
            this.prevBtn.disabled = this.currentPage === 0;
            this.nextBtn.disabled = this.currentPage >= this.totalPages - 1;

            this.prevBtn.style.opacity = this.currentPage === 0 ? '0.5' : '1';
            this.nextBtn.style.opacity = this.currentPage >= this.totalPages - 1 ? '0.5' : '1';
            this.prevBtn.style.cursor = this.currentPage === 0 ? 'not-allowed' : 'pointer';
            this.nextBtn.style.cursor = this.currentPage >= this.totalPages - 1 ? 'not-allowed' : 'pointer';
        }
    }
    
    next() {
        if (this.currentPage < this.totalPages - 1 && !this.isUpdating) {
            this.currentPage++;
            this.updateSliderPosition();
            this.updateButtons();
            this.triggerCustomEvent('slideChanged', this.currentPage);
        }
    }
    
    prev() {
        if (this.currentPage > 0 && !this.isUpdating) {
            this.currentPage--;
            this.updateSliderPosition();
            this.updateButtons();
            this.triggerCustomEvent('slideChanged', this.currentPage);
        }
    }
    
    attachEvents() {
        if (this.prevBtn) {
            const newPrevBtn = this.prevBtn.cloneNode(true);
            this.prevBtn.parentNode.replaceChild(newPrevBtn, this.prevBtn);
            this.prevBtn = newPrevBtn;
            this.prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.prev();
            });
        }
        
        if (this.nextBtn) {
            const newNextBtn = this.nextBtn.cloneNode(true);
            this.nextBtn.parentNode.replaceChild(newNextBtn, this.nextBtn);
            this.nextBtn = newNextBtn;
            this.nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.next();
            });
        }

        this.container.addEventListener('keydown', (e) => {
            if (e.target === this.prevBtn || e.target === this.nextBtn) {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    this.prev();
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    this.next();
                }
            }
        });

        let touchStartX = 0;
        let touchEndX = 0;
        
        this.container.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        this.container.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            const swipeDistance = touchEndX - touchStartX;
            
            if (Math.abs(swipeDistance) > 50) {
                if (swipeDistance > 0) {
                    this.prev();
                } else {
                    this.next();
                }
            }
        });
    }
    
    handleResize() {
        clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(() => {
            this.updateVisibleItems();
        }, 150);
    }
    
    triggerCustomEvent(eventName, detail) {
        const event = new CustomEvent(eventName, { detail: { slider: this, value: detail } });
        this.container.dispatchEvent(event);
    }
    
    goToPage(page) {
        if (page >= 0 && page < this.totalPages && !this.isUpdating) {
            this.currentPage = page;
            this.updateSliderPosition();
            this.updateButtons();
        }
    }
    
    refresh() {
        this.items = Array.from(this.track.children);
        this.totalItems = this.items.length;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        this.currentPage = 0;
        this.updateSliderPosition();
        this.updateButtons();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const sliders = [];
    const sliderContainers = document.querySelectorAll('.slider-container');
    
    sliderContainers.forEach((container, index) => {
        if (!container.classList.contains('slider-initialized')) {
            const slider = new ProductSlider(container, 5);
            sliders.push(slider);
            container.classList.add('slider-initialized');
            container.setAttribute('data-slider-id', index);
        }
    });

    window.productSliders = sliders;
});