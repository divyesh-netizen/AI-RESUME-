"""
Preloaded sample resumes and job descriptions for rapid testing and realistic SaaS demonstrations.
"""

SAMPLE_DATA = {
    "frontend_dev": {
        "title": "Senior Frontend Engineer (React / TypeScript)",
        "candidate_name": "Alex Morgan",
        "resume": """ALEX MORGAN
Email: alex.morgan.dev@example.com | Phone: (555) 382-9912 | Location: San Francisco, CA | Portfolio: alexmorgan.dev | GitHub: github.com/alexmorgan

PROFESSIONAL SUMMARY
Senior Frontend Engineer with 6+ years of experience building high-performance, accessible, and scalable web applications. Expert in React, TypeScript, Next.js, and modern CSS architectures. Proven track record of optimizing Core Web Vitals, leading frontend architecture modernization, and mentoring engineering teams in Agile environments.

TECHNICAL SKILLS
• Languages: TypeScript, JavaScript (ES6+), HTML5, CSS3, SQL, Python
• Frontend: React, Next.js, Redux Toolkit, Zustand, Tailwind CSS, Material UI, GraphQL, Webpack, Vite, Framer Motion
• Testing: Jest, React Testing Library, Cypress, Playwright
• Cloud & Tools: Git, GitHub Actions, Docker, AWS (S3, CloudFront), Figma, Agile/Scrum, CI/CD, REST APIs

PROFESSIONAL EXPERIENCE
Senior Frontend Developer | TechNova Solutions | San Francisco, CA | 2022 - Present
• Spearheaded frontend architecture redesign using Next.js and TypeScript, reducing initial bundle size by 44% and boosting Lighthouse performance score from 62 to 96.
• Engineered a shared design system of 40+ accessible React components with Tailwind CSS, adopted across 5 product teams and increasing sprint velocity by 30%.
• Implemented client-side caching with React Query and optimized GraphQL queries, lowering page load times by 1.8s for over 250,000 monthly active users.
• Mentored 4 junior and mid-level engineers, established frontend testing standards, and increased unit test coverage from 45% to 88% using Jest and Cypress.

Frontend Software Engineer | CloudScale Inc. | Austin, TX | 2019 - 2022
• Developed responsive SaaS analytics dashboard using React, Redux, and D3.js, rendering real-time streaming data for 15,000+ concurrent enterprise users.
• Automated end-to-end integration tests using Cypress in GitHub Actions CI/CD pipeline, decreasing production regression bugs by 35%.
• Collaborated closely with Product Managers and UI/UX designers in 2-week Agile sprints to deliver 18 major product feature releases on schedule.

EDUCATION
Bachelor of Science in Computer Science | University of California, Berkeley | 2015 - 2019
""",
        "job_description": """Position: Senior Frontend Engineer
Company: Apex Innovations
Location: Remote / San Francisco, CA

ABOUT THE ROLE
We are seeking an experienced Senior Frontend Engineer to lead the development of our next-generation SaaS workflow automation platform. You will architect intuitive user interfaces, champion web performance best practices, and work closely with product and design teams.

RESPONSIBILITIES
• Architect, build, and maintain scalable frontend applications using React, TypeScript, Next.js, and Tailwind CSS.
• Collaborate with backend engineers to integrate GraphQL and RESTful APIs with sub-second latency.
• Establish best-in-class unit and end-to-end testing practices using Jest and Cypress or Playwright.
• Optimize application performance, Core Web Vitals, and accessibility (WCAG 2.1 compliance).
• Participate in code reviews, technical design discussions, and mentor fellow software engineers.

REQUIREMENTS & QUALIFICATIONS
• 5+ years of professional software development experience specializing in frontend web development.
• Deep proficiency in TypeScript, JavaScript, React, and Next.js.
• Strong experience with modern CSS frameworks (Tailwind CSS, styled-components).
• Solid understanding of state management (Redux, Zustand) and API integration (GraphQL, REST APIs).
• Experience with CI/CD automation, Docker, and AWS cloud hosting (S3/CloudFront).
• Excellent communication skills and enthusiasm for Agile/Scrum methodologies.
"""
    },
    "fullstack_dev": {
        "title": "Full Stack Engineer (Python & React)",
        "candidate_name": "Samantha Chen",
        "resume": """SAMANTHA CHEN
Email: samantha.chen@devmail.io | Phone: (415) 890-4421 | Seattle, WA | LinkedIn: linkedin.com/in/samanthachen | GitHub: github.com/schen-dev

EXECUTIVE SUMMARY
Full Stack Software Engineer with 5+ years of experience designing and deploying distributed web applications and microservices. Proficient across Python, FastAPI, Django, PostgreSQL, React, and AWS cloud infrastructure. Passionate about API design, database performance tuning, and clean architecture.

CORE PROFICIENCIES
• Programming: Python, TypeScript, JavaScript, SQL, Bash
• Backend & APIs: FastAPI, Django, Flask, Node.js, RESTful APIs, GraphQL, Celery, Redis, RabbitMQ, JWT Authentication
• Frontend: React, Next.js, Tailwind CSS, HTML5, CSS3, Redux Toolkit
• Databases: PostgreSQL, MongoDB, Redis, SQLAlchemy, Prisma
• Cloud & DevOps: AWS (EC2, ECS, RDS, S3, Lambda), Docker, Kubernetes, CI/CD, GitHub Actions, Terraform, Linux

WORK EXPERIENCE
Lead Full Stack Engineer | Apex Financial Tech | Seattle, WA | 2021 - Present
• Architected high-throughput payment processing microservice in FastAPI and PostgreSQL, processing $12M+ in monthly transactions with 99.99% uptime.
• Built interactive real-time trader dashboard with React and WebSockets, cutting state synchronization delays by 60%.
• Optimized database queries and implemented multi-tier Redis caching, reducing average API response latency from 420ms to 65ms.
• Containerized full application stack with Docker and orchestrated AWS ECS deployment via Terraform and GitHub Actions.

Software Engineer | NextWave Software | San Jose, CA | 2018 - 2021
• Developed REST APIs with Python Django and PostgreSQL serving 100,000+ active mobile and web clients.
• Built reusable frontend dashboard modules using React, TypeScript, and Material UI.
• Spearheaded automated CI/CD pipeline implementation, reducing deployment cycle times from 2 days to 15 minutes.

EDUCATION & CERTIFICATIONS
• B.S. in Software Engineering, University of Washington (2014 - 2018)
• AWS Certified Solutions Architect – Associate (2023)
""",
        "job_description": """Role: Senior Full Stack Engineer (Python / React / AWS)
Company: FinScale Global

Job Description:
FinScale is hiring a Senior Full Stack Engineer to build our scalable financial intelligence platform.

Key Responsibilities:
• Design and build robust backend microservices using Python (FastAPI / Django) and PostgreSQL.
• Develop responsive, accessible web interfaces in React and TypeScript with Tailwind CSS.
• Manage cloud infrastructure on AWS (ECS, Lambda, RDS, S3) using Docker and Terraform.
• Implement asynchronous task queues with Celery, Redis, and message brokers (Kafka/RabbitMQ).
• Lead architecture discussions, enforce high test coverage, and promote DevOps best practices.

Requirements:
• 4+ years building full stack web applications with Python and React.
• Strong knowledge of PostgreSQL database indexing, schema design, and query optimization.
• Hands-on experience with Docker, CI/CD pipelines, and AWS cloud services.
• Experience building secure RESTful APIs, OAuth2/JWT authentication, and microservices architecture.
• Strong problem-solving mindset and excellent cross-functional collaboration skills.
"""
    },
    "ai_engineer": {
        "title": "AI & Machine Learning Engineer",
        "candidate_name": "Dr. Marcus Vance",
        "resume": """DR. MARCUS VANCE
Email: marcus.vance.ai@quantummail.com | Phone: (617) 504-2289 | Boston, MA | Google Scholar: scholar.google.com/marcusvance

SUMMARY
AI/ML Engineer and Data Scientist with 6+ years of research and production experience in Natural Language Processing (NLP), Large Language Models (LLMs), RAG pipelines, and deep learning architectures. Proven track record deploying scalable ML inference pipelines on AWS and Kubernetes.

TECHNICAL TOOLKIT
• Languages: Python, C++, SQL, R, Bash
• AI & ML Frameworks: PyTorch, TensorFlow, HuggingFace Transformers, LangChain, LlamaIndex, Scikit-learn, OpenCV
• Data & MLOps: Pandas, NumPy, SciPy, MLflow, Ray, Airflow, Docker, Kubernetes, Triton Inference Server, AWS SageMaker
• Vector Databases: Pinecone, ChromaDB, Weaviate, Qdrant, Milvus
• Backend: FastAPI, Flask, REST APIs, Celery, Redis, PostgreSQL

EXPERIENCE
Staff AI Engineer | DeepCognition Labs | Boston, MA | 2022 - Present
• Designed and deployed an enterprise Retrieval-Augmented Generation (RAG) system using LangChain, Pinecone, and HuggingFace LLMs, serving 80,000+ daily internal queries with 94% retrieval accuracy.
• Fine-tuned open-source LLMs (Llama 3, Mistral) using LoRA/QLoRA on multi-GPU AWS clusters, reducing model inference latency by 52% and cutting API token costs by $18,000/month.
• Built automated data processing and model evaluation pipeline with Apache Airflow and MLflow, tracking 150+ experiment metrics.

Machine Learning Engineer | BioAnalytics AI | Cambridge, MA | 2019 - 2022
• Developed NLP transformer models (BERT, RoBERTa) for biomedical text classification, achieving 96.2% F1-score and outperforming baseline models by 14%.
• Containerized and deployed high-throughput PyTorch model endpoints on Kubernetes using Triton Inference Server.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence Focus) | MIT | 2015 - 2019
B.S. in Applied Mathematics & Statistics | Harvard University | 2011 - 2015
""",
        "job_description": """Position: Senior AI / Machine Learning Engineer (LLM & GenAI)
Company: Cognitive Core AI
Location: Boston, MA / Hybrid

About The Role:
Cognitive Core is looking for a Senior AI/ML Engineer to build next-generation Generative AI applications, RAG architectures, and agentic workflows.

What You'll Do:
• Architect, build, and optimize LLM pipelines, RAG systems, and AI agents using LangChain, LlamaIndex, and Vector Databases (Pinecone/ChromaDB).
• Fine-tune and evaluate state-of-the-art open-source LLMs (Llama, Mistral) with PyTorch and Hugging Face.
• Deploy scalable, low-latency AI microservices on AWS/GCP using Docker, Kubernetes, and FastAPI.
• Build automated MLOps pipelines with MLflow, Airflow, and CI/CD tools.

Qualifications:
• 4+ years of professional ML/NLP development experience in Python.
• Strong hands-on expertise with PyTorch, HuggingFace Transformers, and Vector DBs.
• Experience building and scaling LLM / RAG architectures in production environments.
• Solid background in cloud platforms (AWS/GCP), Docker, and REST API development.
"""
    }
}
