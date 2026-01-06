document.addEventListener('DOMContentLoaded', () => {
    const fullNameInput = document.getElementById('fullName');
    const emailUserInput = document.getElementById('emailUser');
    const emailDomainSelect = document.getElementById('emailDomain');
    const phoneInput = document.getElementById('phone');
    const locationInput = document.getElementById('location');
    const linkTextInput = document.getElementById('linkText');
    const linkUrlInput = document.getElementById('linkUrl');

    const previewName = document.getElementById('previewName');
    const previewContact = document.getElementById('previewContact');
    const saveBtn = document.getElementById('saveBtn');
    const generatePdfBtn = document.getElementById('generatePdfBtn');
    const saveStatus = document.getElementById('saveStatus');

    const skillsContainer = document.getElementById('skillsContainer');
    const addSkillBtn = document.getElementById('addSkillBtn');
    const skillsSectionTitleInput = document.getElementById('skillsSectionTitle');

    const experienceContainer = document.getElementById('experienceContainer');
    const addExperienceBtn = document.getElementById('addExperienceBtn');
    const experienceSectionTitleInput = document.getElementById('experienceSectionTitle');
    const previewExperienceSection = document.getElementById('previewExperienceSection');
    const previewExperience = document.getElementById('previewExperience');
    const previewExperienceTitle = document.getElementById('previewExperienceTitle');

    const educationContainer = document.getElementById('educationContainer');
    const addEducationBtn = document.getElementById('addEducationBtn');
    const educationSectionTitleInput = document.getElementById('educationSectionTitle');
    const previewEducationSection = document.getElementById('previewEducationSection');
    const previewEducation = document.getElementById('previewEducation');
    const previewEducationTitle = document.getElementById('previewEducationTitle');

    let skillsCount = 0;
    let educationCount = 0;
    const MAX_SKILLS = 5;
    const MAX_EDUCATION = 5;

    // Font Size Settings
    const experienceDurationInput = document.getElementById('experienceDuration'); // Was missing in original variable block? No, it's dynamic.
    // Wait, let's just add globalFontFamilySelect here
    const globalFontFamilySelect = document.getElementById('globalFontFamily');

    const fontSizeInputs = {
        name: document.getElementById('nameFontSize'),
        contact: document.getElementById('contactFontSize'),
        sectionTitle: document.getElementById('sectionTitleFontSize'),
        skillsContent: document.getElementById('skillsContentFontSize'),
        experienceCompany: document.getElementById('experienceCompanyFontSize'),
        experiencePosition: document.getElementById('experiencePositionFontSize'),
        experienceDuration: document.getElementById('experienceDurationFontSize'),
        experienceBullet: document.getElementById('experienceBulletFontSize'),
        educationInstitution: document.getElementById('educationInstitutionFontSize'),
        educationDegree: document.getElementById('educationDegreeFontSize'),
        educationDate: document.getElementById('educationDateFontSize'),
        educationDescription: document.getElementById('educationDescriptionFontSize')
    };

    const fontSizeValues = {
        name: document.getElementById('nameFontSizeValue'),
        contact: document.getElementById('contactFontSizeValue'),
        sectionTitle: document.getElementById('sectionTitleFontSizeValue'),
        skillsContent: document.getElementById('skillsContentFontSizeValue'),
        experienceCompany: document.getElementById('experienceCompanyFontSizeValue'),
        experiencePosition: document.getElementById('experiencePositionFontSizeValue'),
        experienceDuration: document.getElementById('experienceDurationFontSizeValue'),
        experienceBullet: document.getElementById('experienceBulletFontSizeValue'),
        educationInstitution: document.getElementById('educationInstitutionFontSizeValue'),
        educationDegree: document.getElementById('educationDegreeFontSizeValue'),
        educationDate: document.getElementById('educationDateFontSizeValue'),
        educationDescription: document.getElementById('educationDescriptionFontSizeValue')
    };

    const resetFontSizesBtn = document.getElementById('resetFontSizes');

    // Default font sizes
    const defaultFontSizes = {
        name: 2.5,
        contact: 0.9,
        sectionTitle: 1.2,
        skillsContent: 0.95,
        experienceCompany: 1,
        experiencePosition: 0.95,
        experienceDuration: 0.9,
        experienceBullet: 0.9,
        educationInstitution: 0.95,
        educationDegree: 0.95,
        educationDate: 0.85,
        educationDescription: 0.9
    };


    // Font Family Logic
    if (globalFontFamilySelect) {
        globalFontFamilySelect.addEventListener('change', () => {
            applyFontFamily(globalFontFamilySelect.value);
            saveStatus.textContent = "Cambios sin guardar...";
        });
    }

    function applyFontFamily(fontValue) {
        let cssFont = '"Helvetica Neue", Helvetica, Arial, sans-serif';
        if (fontValue === 'Times-Roman') cssFont = '"Times New Roman", Times, serif';
        else if (fontValue === 'Courier') cssFont = '"Courier New", Courier, monospace';
        else if (fontValue === 'Georgia') cssFont = 'Georgia, serif';

        const previewElement = document.getElementById('cvPreview');
        if (previewElement) {
            previewElement.style.fontFamily = cssFont;
        }
    }


    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Sub-tab Navigation (for Settings)
    const subTabBtns = document.querySelectorAll('.sub-tab-btn');
    const subTabContents = document.querySelectorAll('.sub-tab-content');

    const resetEducationFontSizesBtn = document.getElementById('resetEducationFontSizes');

    // Function to switch tabs
    function switchTab(targetTab) {
        // Remove active class from all tabs and contents
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        // Add active class to clicked tab and corresponding content
        const targetBtn = document.querySelector(`.tab-btn[data-tab="${targetTab}"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
            document.getElementById(targetTab + 'Tab').classList.add('active');

            // Save to localStorage
            localStorage.setItem('activeTab', targetTab);
        }
    }

    // Restore last active tab from localStorage
    const savedTab = localStorage.getItem('activeTab');
    if (savedTab) {
        switchTab(savedTab);
    }

    // Add click event listeners to tab buttons
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    // Sub-tab Navigation Logic
    function switchSubTab(targetSubTab) {
        subTabBtns.forEach(b => b.classList.remove('active'));
        subTabContents.forEach(c => c.classList.remove('active'));

        const targetBtn = document.querySelector(`.sub-tab-btn[data-subtab="${targetSubTab}"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
            document.getElementById(targetSubTab + 'SubTab').classList.add('active');
        }
    }

    subTabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetSubTab = btn.getAttribute('data-subtab');
            switchSubTab(targetSubTab);
        });
    });

    // Skills Management
    function createSkillInput(title = '', description = '') {
        const skillId = `skill_${Date.now()}_${Math.random()}`;
        const skillDiv = document.createElement('div');
        skillDiv.className = 'skill-input-group';
        skillDiv.innerHTML = `
            <input type="text" class="skill-title-input" data-skill-id="${skillId}" 
                   placeholder="Título (ej: Languages & Frameworks)" value="${title}" 
                   style="font-weight: 600; padding: 0.6rem; border-radius: 0.5rem; border: 1px solid var(--text-secondary); background-color: var(--card-bg); color: var(--text-primary); font-size: 0.9rem; width: 35%;" />
            <input type="text" class="skill-description-input" data-skill-id="${skillId}" 
                   placeholder="Descripción (ej: Python, JavaScript, Selenium...)" value="${description}"
                   style="padding: 0.6rem; border-radius: 0.5rem; border: 1px solid var(--text-secondary); background-color: var(--card-bg); color: var(--text-primary); font-size: 0.9rem; flex: 1;" />
            <button class="btn-remove-skill" data-skill-id="${skillId}">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        `;

        skillsContainer.appendChild(skillDiv);
        skillsCount++;

        // Update button state
        updateAddSkillButton();

        // Add event listener to remove button
        const removeBtn = skillDiv.querySelector('.btn-remove-skill');
        removeBtn.addEventListener('click', () => {
            skillDiv.remove();
            skillsCount--;
            updateAddSkillButton();
            updateSkillsPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        });

        // Add input listeners
        const titleInput = skillDiv.querySelector('.skill-title-input');
        const descInput = skillDiv.querySelector('.skill-description-input');

        titleInput.addEventListener('input', () => {
            updateSkillsPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        });

        descInput.addEventListener('input', () => {
            updateSkillsPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        });

        return skillDiv;
    }

    function updateAddSkillButton() {
        if (skillsCount >= MAX_SKILLS) {
            addSkillBtn.disabled = true;
            addSkillBtn.style.opacity = '0.5';
            addSkillBtn.style.cursor = 'not-allowed';
        } else {
            addSkillBtn.disabled = false;
            addSkillBtn.style.opacity = '1';
            addSkillBtn.style.cursor = 'pointer';
        }
    }

    addSkillBtn.addEventListener('click', () => {
        if (skillsCount < MAX_SKILLS) {
            createSkillInput();
            updateSkillsPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        }
    });

    // --- Work Experience Management ---

    function createExperienceInput(data = {}) {
        const expId = `exp_${Date.now()}_${Math.random()}`;
        const expDiv = document.createElement('div');
        expDiv.className = 'experience-entry';
        expDiv.style.cssText = `
            background: var(--card-bg); 
            border: 1px solid var(--text-secondary); /* Fallback */
            border-left: 4px solid #2563eb; 
            border-radius: 8px; 
            padding: 1.25rem; 
            position: relative;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
            margin-bottom: 2rem;
        `;

        // Default values
        const company = data.company || '';
        const position = data.position || '';
        const duration = data.duration || '';
        const responsibilities = data.responsibilities || [];

        expDiv.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div style="flex: 1;">
                     <input type="text" class="exp-company" placeholder="Empresa (ej: Amazon)" value="${company}" 
                        style="font-size: 1.1rem; font-weight: 700; width: 100%; border: none; border-bottom: 2px solid #e5e7eb; padding: 0.5rem 0; background: transparent; outline: none; transition: border-color 0.2s;" 
                        onfocus="this.style.borderColor='#2563eb'" onblur="this.style.borderColor='#e5e7eb'" />
                </div>
                <button class="btn-remove-exp" style="background: none; border: none; color: #ef4444; cursor: pointer; padding: 0.25rem; margin-left: 1rem; opacity: 0.6; transition: opacity 0.2s;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
                <div style="flex: 2;">
                    <label style="display: block; font-size: 0.75rem; color: #666; margin-bottom: 0.25rem; font-weight: 600; text-transform: uppercase;">Puesto</label>
                    <input type="text" class="exp-position" placeholder="Backend Dev" value="${position}" 
                           style="width: 100%; padding: 0.6rem; border-radius: 6px; border: 1px solid #d1d5db; background: #f9fafb; font-size: 0.95rem;" />
                </div>
                <div style="flex: 1;">
                    <label style="display: block; font-size: 0.75rem; color: #666; margin-bottom: 0.25rem; font-weight: 600; text-transform: uppercase;">Periodo</label>
                     <input type="text" class="exp-duration" placeholder="2022 - Presente" value="${duration}" 
                           style="width: 100%; padding: 0.6rem; border-radius: 6px; border: 1px solid #d1d5db; background: #f9fafb; font-size: 0.95rem;" />
                </div>
            </div>
            
            <div class="responsibilities-container" style="background: #f8f9fa; padding: 1rem; border-radius: 6px; border: 1px dashed #ced4da;">
                <label style="display: block; font-size: 0.85rem; color: #374151; margin-bottom: 0.75rem; font-weight: 600;">
                    Logros y Responsabilidades 
                    <span style="font-weight: 400; color: #9ca3af; font-size: 0.8rem;">(Max 5)</span>
                </label>
                <div class="responsibilities-list"></div>
                <button class="btn-add-point" style="background: none; border: none; color: #2563eb; cursor: pointer; font-size: 0.85rem; margin-top: 0.5rem; display: flex; align-items: center; gap: 0.4rem; font-weight: 500; padding: 0.4rem 0;">
                    <div style="background: #eff6ff; padding: 4px; border-radius: 50%;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    </div>
                    Agregar punto clave
                </button>
            </div>
        `;

        // Remove Experience logic
        expDiv.querySelector('.btn-remove-exp').addEventListener('click', () => {
            expDiv.remove();
            updateExperiencePreview();
            saveStatus.textContent = "Cambios sin guardar...";
        });

        // Inputs change listener
        ['exp-company', 'exp-position', 'exp-duration'].forEach(cls => {
            expDiv.querySelector('.' + cls).addEventListener('input', () => {
                updateExperiencePreview();
                saveStatus.textContent = "Cambios sin guardar...";
            });
        });

        // Handle Responsibilities
        const respList = expDiv.querySelector('.responsibilities-list');
        const addPointBtn = expDiv.querySelector('.btn-add-point');

        const addPoint = (text = '') => {
            if (respList.children.length >= 5) return;

            const pointDiv = document.createElement('div');
            pointDiv.style.cssText = 'display: flex; gap: 0.5rem; margin-bottom: 0.5rem; align-items: center; animation: fadeIn 0.3s ease;';
            pointDiv.innerHTML = `
                <div style="color: #9ca3af; display: flex; align-items: center;">•</div>
                <input type="text" class="exp-point-input" value="${text}" placeholder="Desarrollé una API RESTful..." 
                       style="flex: 1; font-size: 0.9rem; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 4px; color: #374151;" />
                <button class="btn-remove-point" style="background: none; border: none; color: #ef4444; cursor: pointer; opacity: 0.5; transition: opacity 0.2s; padding: 0.2rem;">
                     <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
                <style>@keyframes fadeIn { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }</style>
            `;

            // Hover effect for delete button
            const removeBtn = pointDiv.querySelector('.btn-remove-point');
            pointDiv.addEventListener('mouseenter', () => removeBtn.style.opacity = '1');
            pointDiv.addEventListener('mouseleave', () => removeBtn.style.opacity = '0.5');

            pointDiv.querySelector('.btn-remove-point').addEventListener('click', () => {
                pointDiv.remove();
                updateAddPointButton();
                updateExperiencePreview();
                saveStatus.textContent = "Cambios sin guardar...";
            });

            pointDiv.querySelector('.exp-point-input').addEventListener('input', () => {
                updateExperiencePreview();
                saveStatus.textContent = "Cambios sin guardar...";
            });

            respList.appendChild(pointDiv);
            updateAddPointButton();
        };

        const updateAddPointButton = () => {
            if (respList.children.length >= 5) {
                addPointBtn.style.display = 'none';
            } else {
                addPointBtn.style.display = 'flex';
            }
        };

        addPointBtn.addEventListener('click', () => addPoint());

        // Initialize existing points
        responsibilities.forEach(r => addPoint(r));

        experienceContainer.appendChild(expDiv);
    }

    addExperienceBtn.addEventListener('click', () => {
        createExperienceInput();
        updateExperiencePreview();
        saveStatus.textContent = "Cambios sin guardar...";
    });

    function getExperienceData() {
        const entries = [];
        document.querySelectorAll('.experience-entry').forEach(div => {
            const company = div.querySelector('.exp-company').value.trim();
            const position = div.querySelector('.exp-position').value.trim();
            const duration = div.querySelector('.exp-duration').value.trim();

            const points = [];
            div.querySelectorAll('.exp-point-input').forEach(input => {
                if (input.value.trim()) points.push(input.value.trim());
            });

            if (company || position || duration) {
                entries.push({
                    company,
                    position,
                    duration,
                    responsibilities: points
                });
            }
        });
        return entries;
    }

    function updateExperiencePreview() {
        const entries = getExperienceData();
        const titleValue = experienceSectionTitleInput.value.trim();

        previewExperienceTitle.textContent = titleValue || 'WORK EXPERIENCE';

        // Get current font sizes
        const companySize = fontSizeInputs.experienceCompany ? fontSizeInputs.experienceCompany.value : '1';
        const positionSize = fontSizeInputs.experiencePosition ? fontSizeInputs.experiencePosition.value : '0.95';
        const durationSize = fontSizeInputs.experienceDuration ? fontSizeInputs.experienceDuration.value : '0.9';
        const bulletSize = fontSizeInputs.experienceBullet ? fontSizeInputs.experienceBullet.value : '0.9';

        if (entries.length > 0) {
            previewExperienceSection.style.display = 'block';
            previewExperience.innerHTML = '';

            entries.forEach(entry => {
                const entryDiv = document.createElement('div');
                entryDiv.style.marginBottom = '1.2rem';

                let html = `
                    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.4rem;">
                        <div style="flex: 1;">
                            <span style="font-size: ${companySize}rem; color: #2c3e50; font-weight: bold;">${entry.company}</span>
                            ${entry.position ? `<span style="margin: 0 0.5rem; color: #ccc;">|</span><span style="font-size: ${positionSize}rem; font-weight: 600; color: #333;">${entry.position}</span>` : ''}
                        </div>
                         <span style="font-size: ${durationSize}rem; color: #666; font-style: italic; white-space: nowrap; margin-left: 1rem;">${entry.duration}</span>
                    </div>
                `;

                if (entry.responsibilities && entry.responsibilities.length > 0) {
                    html += '<ul style="margin: 0; padding-left: 1.2rem; margin-top: 0.2rem;">';
                    entry.responsibilities.forEach(point => {
                        html += `<li style="font-size: ${bulletSize}rem; color: #444; margin-bottom: 0.4rem;">${point}</li>`;
                    });
                    html += '</ul>';
                }

                entryDiv.innerHTML = html;
                previewExperience.appendChild(entryDiv);
            });
        } else {
            previewExperienceSection.style.display = 'none';
        }
    }

    experienceSectionTitleInput.addEventListener('input', () => {
        updateExperiencePreview();
        saveStatus.textContent = "Cambios sin guardar...";
    });

    // Function to get all skills
    function getAllSkills() {
        const skillGroups = document.querySelectorAll('.skill-input-group');
        const skills = [];
        skillGroups.forEach(group => {
            const titleInput = group.querySelector('.skill-title-input');
            const descInput = group.querySelector('.skill-description-input');

            const title = titleInput ? titleInput.value.trim() : '';
            const description = descInput ? descInput.value.trim() : '';

            // Solo agregar si al menos uno de los campos tiene contenido
            if (title || description) {
                skills.push({
                    title: title,
                    description: description
                });
            }
        });
        return skills;
    }

    // Function to update skills preview
    function updateSkillsPreview() {
        const skills = getAllSkills();
        const previewSkillsSection = document.getElementById('previewSkillsSection');
        const previewSkills = document.getElementById('previewSkills');
        const previewSkillsTitle = document.getElementById('previewSkillsTitle');
        const skillsSectionTitleInput = document.getElementById('skillsSectionTitle');

        // Update section title
        if (skillsSectionTitleInput && skillsSectionTitleInput.value.trim()) {
            previewSkillsTitle.textContent = skillsSectionTitleInput.value.trim();
        } else {
            previewSkillsTitle.textContent = 'TECHNICAL SKILLS';
        }

        if (skills.length > 0) {
            previewSkillsSection.style.display = 'block';
            previewSkills.innerHTML = ''; // Clear previous content

            skills.forEach(skill => {
                const skillDiv = document.createElement('div');
                // Use flex to align bullet and text
                skillDiv.style.display = 'flex';
                skillDiv.style.alignItems = 'baseline';
                skillDiv.style.marginBottom = '0.4rem'; // Gap between skills
                skillDiv.style.lineHeight = '1.4';

                // Bullet
                const bullet = document.createElement('span');
                bullet.textContent = '•';
                bullet.style.marginRight = '0.5rem';
                bullet.style.color = '#333';
                skillDiv.appendChild(bullet);

                // Content container
                const contentSpan = document.createElement('span');

                // Apply current font size
                const sizes = getFontSizes();
                if (sizes.skillsContent) {
                    skillDiv.style.fontSize = sizes.skillsContent + 'rem';
                } else {
                    skillDiv.style.fontSize = '0.95rem';
                }

                let contentHtml = '';
                if (skill.title) {
                    contentHtml += `<strong style="color: #2c3e50;">${skill.title}:</strong> `;
                }
                if (skill.description) {
                    contentHtml += `<span style="color: #333;">${skill.description}</span>`;
                }
                contentSpan.innerHTML = contentHtml;

                skillDiv.appendChild(contentSpan);
                previewSkills.appendChild(skillDiv);
            });

        } else {
            previewSkillsSection.style.display = 'none';
        }
    }

    // --- Education Management (New Single Line Format) ---
    function createEducationInput(institution = '', degree = '', date = '', description = '') {
        const eduId = `edu_${Date.now()}_${Math.random()}`;
        const eduDiv = document.createElement('div');
        eduDiv.className = 'education-input-group';
        eduDiv.style.display = 'flex';
        eduDiv.style.flexDirection = 'column';
        eduDiv.style.gap = '0.5rem';
        eduDiv.style.marginBottom = '1rem';
        eduDiv.style.padding = '0.5rem';
        eduDiv.style.border = '1px solid var(--text-secondary)'; // Light border to group
        eduDiv.style.borderRadius = '0.5rem';

        // Row 1: Institution, Degree, Date
        const row1 = document.createElement('div');
        row1.style.display = 'flex';
        row1.style.gap = '0.5rem';

        row1.innerHTML = `
            <input type="text" class="edu-institution" placeholder="Institución" value="${institution}" 
                   style="flex: 2; font-weight: 600; padding: 0.6rem; border-radius: 0.5rem; border: 1px solid var(--text-secondary); background-color: var(--card-bg); color: var(--text-primary); font-size: 0.9rem;" />
            <input type="text" class="edu-degree" placeholder="Título" value="${degree}"
                   style="flex: 2; padding: 0.6rem; border-radius: 0.5rem; border: 1px solid var(--text-secondary); background-color: var(--card-bg); color: var(--text-primary); font-size: 0.9rem;" />
            <input type="text" class="edu-date" placeholder="Fecha" value="${date}"
                   style="flex: 1; padding: 0.6rem; border-radius: 0.5rem; border: 1px solid var(--text-secondary); background-color: var(--card-bg); color: var(--text-primary); font-size: 0.9rem;" />
        `;

        // Row 2: Description (Optional) + Remove Button
        const row2 = document.createElement('div');
        row2.style.display = 'flex';
        row2.style.gap = '0.5rem';
        row2.style.alignItems = 'center';

        row2.innerHTML = `
            <span style="font-size: 1.2rem; color: #333;">•</span>
            <input type="text" class="edu-description" placeholder="Descripción opcional..." value="${description}"
                   style="flex: 1; padding: 0.6rem; border-radius: 0.5rem; border: 1px solid var(--text-secondary); background-color: var(--card-bg); color: var(--text-primary); font-size: 0.9rem;" />
            <button class="btn-remove-education" style="background: none; border: none; color: #ef4444; cursor: pointer; padding: 0.25rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        `;

        eduDiv.appendChild(row1);
        eduDiv.appendChild(row2);

        educationContainer.appendChild(eduDiv);
        educationCount++;

        updateAddEducationButton();

        // Listeners
        const removeBtn = row2.querySelector('.btn-remove-education');
        removeBtn.addEventListener('click', () => {
            eduDiv.remove();
            educationCount--;
            updateAddEducationButton();
            updateEducationPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        });

        const inputs = eduDiv.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                updateEducationPreview();
                saveStatus.textContent = "Cambios sin guardar...";
            });
        });

        return eduDiv;
    }

    function updateAddEducationButton() {
        if (educationCount >= MAX_EDUCATION) {
            addEducationBtn.disabled = true;
            addEducationBtn.style.opacity = '0.5';
            addEducationBtn.style.cursor = 'not-allowed';
        } else {
            addEducationBtn.disabled = false;
            addEducationBtn.style.opacity = '1';
            addEducationBtn.style.cursor = 'pointer';
        }
    }

    addEducationBtn.addEventListener('click', () => {
        if (educationCount < MAX_EDUCATION) {
            createEducationInput();
            updateEducationPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        }
    });

    educationSectionTitleInput.addEventListener('input', () => {
        updateEducationPreview();
        saveStatus.textContent = "Cambios sin guardar...";
    });

    function getAllEducation() {
        const eduGroups = document.querySelectorAll('.education-input-group');
        const education = [];
        eduGroups.forEach(group => {
            const institution = group.querySelector('.edu-institution').value.trim();
            const degree = group.querySelector('.edu-degree').value.trim();
            const date = group.querySelector('.edu-date').value.trim();
            const description = group.querySelector('.edu-description').value.trim();

            if (institution || degree || date || description) {
                education.push({
                    institution,
                    degree,
                    date,
                    description
                });
            }
        });
        return education;
    }

    function updateEducationPreview() {
        const education = getAllEducation();

        // Update section title
        if (educationSectionTitleInput && educationSectionTitleInput.value.trim()) {
            previewEducationTitle.textContent = educationSectionTitleInput.value.trim();
        } else {
            previewEducationTitle.textContent = 'EDUCATION';
        }

        if (education.length > 0) {
            previewEducationSection.style.display = 'block';
            previewEducation.innerHTML = '';

            education.forEach(edu => {
                const eduDiv = document.createElement('div');
                eduDiv.style.marginBottom = '0.6rem';
                eduDiv.style.lineHeight = '1.4';

                // First Line: Institution - Degree - Date
                const firstLine = document.createElement('div');
                firstLine.style.display = 'flex';
                firstLine.style.alignItems = 'baseline';
                firstLine.style.flexWrap = 'wrap';

                // Get custom font sizes
                const sizes = getFontSizes();
                const institutionSize = sizes.educationInstitution || 0.95;
                const degreeSize = sizes.educationDegree || 0.95;
                const dateSize = sizes.educationDate || 0.85;
                const descriptionSize = sizes.educationDescription || 0.9;

                // HTML Construction
                let html = '';
                if (edu.institution) {
                    html += `<strong style="color: #2c3e50; font-size: ${institutionSize}rem;">${edu.institution}</strong>`;
                }
                if (edu.degree) {
                    const sep = edu.institution ? '<span style="margin: 0 0.5rem; color: #ccc;">|</span>' : '';
                    html += `${sep}<span style="color: #333; font-size: ${degreeSize}rem;">${edu.degree}</span>`;
                }
                if (edu.date) {
                    const sep = (edu.institution || edu.degree) ? '<span style="margin: 0 0.5rem; color: #ccc;">|</span>' : '';
                    html += `${sep}<span style="color: #666; font-style: italic; font-size: ${dateSize}rem;">${edu.date}</span>`;
                }
                firstLine.innerHTML = html;
                eduDiv.appendChild(firstLine);

                // Second Line: Description (Optional)
                if (edu.description) {
                    const secondLine = document.createElement('div');
                    secondLine.style.display = 'flex';
                    secondLine.style.alignItems = 'baseline';
                    secondLine.style.marginTop = '0.1rem';

                    const bullet = document.createElement('span');
                    bullet.textContent = '•';
                    bullet.style.marginRight = '0.5rem';
                    bullet.style.color = '#333';
                    bullet.style.fontSize = `${descriptionSize}rem`;
                    secondLine.appendChild(bullet);

                    const descSpan = document.createElement('span');
                    descSpan.style.color = '#444';
                    descSpan.style.fontSize = `${descriptionSize}rem`;
                    descSpan.textContent = edu.description;
                    secondLine.appendChild(descSpan);

                    eduDiv.appendChild(secondLine);
                }

                previewEducation.appendChild(eduDiv);
            });

        } else {
            previewEducationSection.style.display = 'none';
        }
    }

    // Font Size Management Functions
    function applyFontSizes(sizes) {
        // Apply to preview elements
        if (previewName) {
            previewName.style.fontSize = sizes.name + 'rem';
        }
        if (previewContact) {
            previewContact.style.fontSize = sizes.contact + 'rem';
        }

        // Section titles
        const sectionTitles = document.querySelectorAll('.cv-section-title');
        sectionTitles.forEach(title => {
            title.style.fontSize = sizes.sectionTitle + 'rem';
        });

        // Skills content
        const skillDivs = document.querySelectorAll('#previewSkills > div');
        skillDivs.forEach(div => {
            div.style.fontSize = sizes.skillsContent + 'rem';
        });

        updateExperiencePreview();
        updateEducationPreview();
    }

    function updateFontSizeDisplay(key, value) {
        if (fontSizeValues[key]) {
            fontSizeValues[key].textContent = value + 'rem';
        }
    }

    function setupFontSizeListeners() {
        Object.keys(fontSizeInputs).forEach(key => {
            const input = fontSizeInputs[key];
            if (input) {
                input.addEventListener('input', (e) => {
                    const value = parseFloat(e.target.value);
                    updateFontSizeDisplay(key, value);

                    const sizes = {};
                    Object.keys(fontSizeInputs).forEach(k => {
                        sizes[k] = parseFloat(fontSizeInputs[k].value);
                    });

                    applyFontSizes(sizes);
                    saveStatus.textContent = "Cambios sin guardar...";
                });
            }
        });
    }

    function resetFontSizes() {
        Object.keys(defaultFontSizes).forEach(key => {
            if (fontSizeInputs[key]) {
                fontSizeInputs[key].value = defaultFontSizes[key];
                updateFontSizeDisplay(key, defaultFontSizes[key]);
            }
        });
        applyFontSizes(defaultFontSizes);
        saveStatus.textContent = "Cambios sin guardar...";
    }

    function loadFontSizes(data) {
        if (data.fontSizes) {
            Object.keys(data.fontSizes).forEach(key => {
                if (fontSizeInputs[key]) {
                    const value = data.fontSizes[key];
                    fontSizeInputs[key].value = value;
                    updateFontSizeDisplay(key, value);
                }
            });
            applyFontSizes(data.fontSizes);
        } else {
            applyFontSizes(defaultFontSizes);
        }
    }

    function getFontSizes() {
        const sizes = {};
        Object.keys(fontSizeInputs).forEach(key => {
            sizes[key] = parseFloat(fontSizeInputs[key].value);
        });
        return sizes;
    }

    // Setup font size listeners
    setupFontSizeListeners();

    // Reset button
    if (resetFontSizesBtn) {
        resetFontSizesBtn.addEventListener('click', resetFontSizes);
    }

    // Reset Education Font Sizes
    function resetEducationFontSizes() {
        const educationKeys = ['educationInstitution', 'educationDegree', 'educationDate', 'educationDescription'];
        educationKeys.forEach(key => {
            if (fontSizeInputs[key]) {
                fontSizeInputs[key].value = defaultFontSizes[key];
                updateFontSizeDisplay(key, defaultFontSizes[key]);
            }
        });
        const sizes = getFontSizes();
        applyFontSizes(sizes);
        saveStatus.textContent = "Cambios sin guardar...";
    }

    if (resetEducationFontSizesBtn) {
        resetEducationFontSizesBtn.addEventListener('click', resetEducationFontSizes);
    }


    // Función para actualizar el preview de contacto
    function updateContactPreview() {
        const contactParts = [];

        // Email completo
        if (emailUserInput.value) {
            const fullEmail = `${emailUserInput.value}@${emailDomainSelect.value}`;
            contactParts.push(`<span>${fullEmail}</span>`);
        }

        if (phoneInput.value) {
            contactParts.push(`<span>${phoneInput.value}</span>`);
        }

        if (locationInput.value) {
            contactParts.push(`<span>${locationInput.value}</span>`);
        }

        // Link con hipervínculo
        if (linkTextInput.value && linkUrlInput.value) {
            contactParts.push(`<span><a href="${linkUrlInput.value}" target="_blank" style="color: #2563eb; text-decoration: underline;">${linkTextInput.value}</a></span>`);
        } else if (linkTextInput.value) {
            contactParts.push(`<span>${linkTextInput.value}</span>`);
        }

        if (contactParts.length > 0) {
            previewContact.innerHTML = contactParts.join('<span style="margin: 0 0.5rem;">|</span>');
        } else {
            previewContact.innerHTML = '<span style="color: #999;">Agrega tu información de contacto</span>';
        }
    }

    // Load initial data
    fetch('/get_cv_data')
        .then(response => response.json())
        .then(data => {
            if (data.fullName) {
                fullNameInput.value = data.fullName;
                previewName.textContent = data.fullName;
            } else {
                previewName.textContent = "Tu Nombre";
            }

            // Cargar email dividido
            if (data.emailUser) emailUserInput.value = data.emailUser;
            if (data.emailDomain) emailDomainSelect.value = data.emailDomain;

            if (data.phone) phoneInput.value = data.phone;
            if (data.location) locationInput.value = data.location;

            // Cargar link dividido
            if (data.linkText) linkTextInput.value = data.linkText;
            if (data.linkUrl) linkUrlInput.value = data.linkUrl;

            // Load skills section title
            if (data.skillsSectionTitle) {
                skillsSectionTitleInput.value = data.skillsSectionTitle;
            }

            // Load skills
            if (data.skills && Array.isArray(data.skills)) {
                data.skills.forEach(skill => {
                    if (typeof skill === 'object' && skill !== null) {
                        // Nuevo formato: objeto con title y description
                        createSkillInput(skill.title || '', skill.description || '');
                    } else {
                        // Formato antiguo: string simple (para compatibilidad)
                        createSkillInput('', skill);
                    }
                });
            }

            updateContactPreview();
            updateSkillsPreview();

            // Load Experience
            if (data.experienceSectionTitle) {
                experienceSectionTitleInput.value = data.experienceSectionTitle;
            }

            if (data.experience && Array.isArray(data.experience)) {
                data.experience.forEach(exp => createExperienceInput(exp));
            }
            updateExperiencePreview();

            // Load Education
            if (data.educationSectionTitle) {
                educationSectionTitleInput.value = data.educationSectionTitle;
            }

            if (data.education && Array.isArray(data.education)) {
                data.education.forEach(edu => {
                    // Check if matches new format or old to prevent error (though we reset json)
                    createEducationInput(edu.institution || '', edu.degree || '', edu.date || '', edu.description || '');
                });
            }
            updateEducationPreview();

            // Load font sizes
            loadFontSizes(data);

            // Load Font Family
            if (data.fontFamily) {
                if (globalFontFamilySelect) globalFontFamilySelect.value = data.fontFamily;
                applyFontFamily(data.fontFamily);
            }
        })
        .catch(err => console.error('Error loading data:', err));

    // Real-time preview update for name
    fullNameInput.addEventListener('input', (e) => {
        const value = e.target.value;
        previewName.textContent = value || "Tu Nombre";
        saveStatus.textContent = "Cambios sin guardar...";
    });

    // Real-time preview update for contact fields
    [emailUserInput, emailDomainSelect, phoneInput, locationInput, linkTextInput, linkUrlInput].forEach(input => {
        input.addEventListener('input', () => {
            updateContactPreview();
            saveStatus.textContent = "Cambios sin guardar...";
        });
        // Para el select, también escuchar el evento change
        if (input.tagName === 'SELECT') {
            input.addEventListener('change', () => {
                updateContactPreview();
                saveStatus.textContent = "Cambios sin guardar...";
            });
        }
    });

    // Real-time preview update for skills section title
    skillsSectionTitleInput.addEventListener('input', () => {
        updateSkillsPreview();
        saveStatus.textContent = "Cambios sin guardar...";
    });

    // Save Data
    saveBtn.addEventListener('click', () => {
        const data = {
            fullName: fullNameInput.value,
            emailUser: emailUserInput.value,
            emailDomain: emailDomainSelect.value,
            phone: phoneInput.value,
            location: locationInput.value,
            linkText: linkTextInput.value,
            linkUrl: linkUrlInput.value,
            skillsSectionTitle: skillsSectionTitleInput.value || 'TECHNICAL SKILLS',
            skills: getAllSkills(),
            experience: getExperienceData(),
            educationSectionTitle: educationSectionTitleInput.value || 'EDUCATION',
            education: getAllEducation(),
            fontSizes: getFontSizes(),
            fontFamily: globalFontFamilySelect ? globalFontFamilySelect.value : 'Helvetica'
        };

        saveStatus.textContent = "Guardando...";
        saveBtn.disabled = true;

        fetch('/save_cv_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    saveStatus.textContent = "¡Guardado!";
                    setTimeout(() => { saveStatus.textContent = ""; }, 2000);
                } else {
                    saveStatus.textContent = "Error al guardar";
                }
            })
            .catch(err => {
                console.error('Error saving:', err);
                saveStatus.textContent = "Error de conexión";
            })
            .finally(() => {
                saveBtn.disabled = false;
            });
    });

    // Generate PDF
    generatePdfBtn.addEventListener('click', () => {
        const data = {
            fullName: fullNameInput.value,
            emailUser: emailUserInput.value,
            emailDomain: emailDomainSelect.value,
            phone: phoneInput.value,
            location: locationInput.value,
            linkText: linkTextInput.value,
            linkUrl: linkUrlInput.value,
            skillsSectionTitle: skillsSectionTitleInput.value || 'TECHNICAL SKILLS',
            skills: getAllSkills(),
            experience: getExperienceData(),
            educationSectionTitle: educationSectionTitleInput.value || 'EDUCATION',
            education: getAllEducation(),
            fontSizes: getFontSizes(),
            fontFamily: globalFontFamilySelect ? globalFontFamilySelect.value : 'Helvetica'
        };

        generatePdfBtn.disabled = true;
        const originalText = generatePdfBtn.querySelector('span').lastChild.textContent;
        generatePdfBtn.querySelector('span').lastChild.textContent = ' Generando...';

        fetch('/generate_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (response.ok) {
                    return response.blob();
                }
                throw new Error('Error al generar PDF');
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                let filename = 'mi_cv.pdf';
                if (data.fullName) {
                    const cleanedName = data.fullName.replace(/[^a-zA-Z0-9]/g, '');
                    if (cleanedName) {
                        filename = `${cleanedName}CV.pdf`;
                    }
                }
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            })
            .catch(err => {
                console.error('Error:', err);
                alert('Hubo un error al generar el PDF.');
            })
            .finally(() => {
                generatePdfBtn.disabled = false;
                generatePdfBtn.querySelector('span').lastChild.textContent = originalText;
            });
    });
});
