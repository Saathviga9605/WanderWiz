document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('preferences-form');
    const resultsDiv = document.getElementById('results');
    const experienceInput = document.getElementById('experience-input');
    const dropdownContent = document.getElementById('dropdown-content');
    const selectedOptionsDiv = document.getElementById('selected-options');
    const dietaryRestrictionsSelect = document.getElementById('dietary-restrictions');
    const dietaryRestrictionsDetail = document.getElementById('dietary-restrictions-detail');

    async function updateImage() {
        const imageElement = document.getElementById('dynamic-image');
        while (true) {
            imageElement.src = `https://source.unsplash.com/800x400/?travel&${Math.random()}`;
            await new Promise(resolve => setTimeout(resolve, 3000));
        }
    }

    updateImage();

    const experiences = [
        "Serene Relaxation",
        "Thrilling Adventures",
        "Cultural Museums",
        "Historic Exploration",
        "Breathtaking Natural Wonders",
        "Urban Exploration",
        "Authentic Rural Life",
        "Beachfront Relaxation",
        "Mountain Escapades",
        "Festive Celebrations",
        "Wildlife Encounters",
        "Local Markets and Shopping",
        "Adventure Sports",
        "Scenic Cruises",
        "Wellness and Spa Retreats",
        "Gastronomic Journeys",
        "Art and Craft Workshops",
        "Volunteer Experiences",
        "Nightlife and Entertainment",
        "Spiritual and Meditation Retreats",
        "Local Traditions and Customs",
        "Unique Stays",
    ];
    
    let selectedExperiences = [];

    function renderDropdown() {
        dropdownContent.innerHTML = experiences
            .filter(exp => !selectedExperiences.includes(exp))
            .map(exp => `<div class="dropdown-item" data-value="${exp}">${exp}</div>`) 
            .join('');
    }
    
    function renderSelectedOptions() {
        selectedOptionsDiv.innerHTML = selectedExperiences
            .map(exp => `<div class="selected-item" data-value="${exp}">${exp} <span class="remove-item">×</span></div>`)
            .join('');
    }    

    function renderSelectedOptions() {
        selectedOptionsDiv.innerHTML = selectedExperiences
            .map(exp => `<div class="selected-item" data-value="${exp}">${exp} <span class="remove-item">×</span></div>`) 
            .join('');
    }

    function handleDropdownClick(event) {
        if (event.target.classList.contains('dropdown-item')) {
            const value = event.target.dataset.value;
            if (selectedExperiences.length < 3) {
                selectedExperiences.push(value);
                renderSelectedOptions();
                renderDropdown();
            }
        }
    }

    function handleSelectedOptionsClick(event) {
        if (event.target.classList.contains('remove-item')) {
            const value = event.target.parentElement.dataset.value;
            selectedExperiences = selectedExperiences.filter(exp => exp !== value);
            renderSelectedOptions();
            renderDropdown();
        }
    }

    function handleDietaryRestrictionsChange() {
        if (dietaryRestrictionsSelect.value === 'Yes') {
            dietaryRestrictionsDetail.style.display = 'block';
        } else {
            dietaryRestrictionsDetail.style.display = 'none';
        }
    }

    experienceInput.addEventListener('click', () => {
        dropdownContent.style.display = 'block';
    });

    document.addEventListener('click', (event) => {
        if (!document.querySelector('.dropdown-container').contains(event.target)) {
            dropdownContent.style.display = 'none';
        }
    });

    dropdownContent.addEventListener('click', handleDropdownClick);
    selectedOptionsDiv.addEventListener('click', handleSelectedOptionsClick);
    dietaryRestrictionsSelect.addEventListener('change', handleDietaryRestrictionsChange);

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const data = {
            destination: formData.get('destination'),
            sourceCity: formData.get('source-city'), 
            experience: selectedExperiences,
            transportation: formData.get('transportation').split(',').map(mode => mode.trim()),
            travelStyle: formData.get('travel-style'),
            dietaryRestrictions: formData.get('dietary-restrictions'),
            dietaryDetails: formData.get('dietary-details'),
            month: formData.get('month'),
            budget: formData.get('budget'),
            interests: formData.get('interests').split(',').map(interest => interest.trim()),
            duration: formData.get('duration')
        };
        
        try {
            const response = await fetch('/generate-itinerary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            console.log("API response:", result); 
            if (result.itinerary) {
                sessionStorage.setItem('itinerary', result.itinerary);
                window.location.href = '/result';
            } else {
                alert('No itinerary found.');
            }
        } catch (error) {
            alert('Error generating itinerary. Please try again.');
        }
    });
    
    renderDropdown();
});
