(function(){
  var dict = {
    pt: {
      // landing
      'landing.nav.courses': 'CURSOS',
      'landing.nav.programs': 'PROGRAMAS',
      'landing.nav.community': 'COMUNIDADE',
      'landing.nav.mycourses': 'OS MEUS CURSOS',
      'landing.nav.openpanel': 'Abrir painel',
      'landing.nav.login': 'ENTRAR',
      'landing.nav.signup': 'Criar conta',
      'landing.hero.title': 'GARANTE SEU FUTURO APRENDENDO NOVAS HABILIDADES ONLINE.',
      'landing.hero.subtitle': 'Junta-te a milhares de estudantes e aprende com cursos práticos, ao teu ritmo, com certificado profissional.',
      'landing.hero.cta': 'Começar agora',
      'landing.band.title': 'APRENDE AS TECNOLOGIAS USADAS NAS MELHORES EMPRESAS DE SOFTWARE DO MUNDO',
      'landing.band.desc': 'Domina as ferramentas que as grandes empresas usam todos os dias — do backend ao frontend, com projetos reais e tecnologias modernas.',
      'landing.courses.title': 'Escolha o seu curso...',
      'landing.courses.explore': 'Explore Todos Os Cursos ⟶',
      'landing.careers.title': 'DESENVOLVEMOS CARREIRAS ATRAVÉS DA EDUCAÇÃO',
      'landing.careers.subtitle': 'Subscreve e recebe novidades',
      'landing.careers.placeholder': 'O teu e-mail',
      'landing.careers.btn': 'SUBSCREVER',
      'landing.footer.nav': 'Navegação',
      'landing.footer.courses': 'Cursos',
      'landing.footer.about': 'Sobre',
      'landing.footer.copy': '© 2026 Academy. Todos os direitos reservados.',
      // dashboard
      'dash.search.placeholder': 'Pesquisar aulas, produtos digitais, professores',
      'dash.mycourses': 'My Classes',
      'dash.allclasses': 'All Classes',
      'dash.discover': 'Discover',
      'dash.results': 'Results',
      'dash.noclasses': 'No classes found',
      'dash.noclasses.sub': 'Try a different search or category.',
      'dash.explore': 'Explore',
      'dash.learn': 'Learn',
      'dash.saved': 'Saved',
      'dash.profile': 'Profile',
      'dash.signin': 'Entrar',
      'dash.signup': 'Criar conta',
      'dash.notification.title': 'Notificações',
      'dash.notification.empty': 'Sem notificações ainda.',
      'dash.signout': 'Terminar sessão',
      // auth
      'login.title': 'Iniciar sessão',
      'login.subtitle': 'Bem-vindo de volta. Inicie sessão para continuar',
      'signup.title': 'Criar conta',
      'signup.subtitle': 'Crie a sua conta para continuar',
      'oauth.github': 'Continuar com GitHub',
      'oauth.google': 'Continuar com Google',
      'oauth.agentmail': 'Continuar com AgentMail',
      'divider.or': 'ou',
      'field.email': 'E-mail',
      'field.password': 'Palavra-passe',
      'field.firstname': 'Nome',
      'field.lastname': 'Apelido',
      'field.confirm': 'Confirmar palavra-passe',
      'forgot': 'Esqueceu a palavra-passe?',
      'hint.password': 'Use 8–32 caracteres com maiúsculas, minúsculas, número e caractere especial.',
      'placeholder.email': 'exemplo@email.com',
      'placeholder.password.login': '•••••',
      'placeholder.password.create': 'Crie uma palavra-passe forte',
      'placeholder.password.confirm': 'Confirme a sua palavra-passe',
      'btn.signin': 'Entrar',
      'btn.signup': 'Criar conta',
      'footer.noaccount': 'Não tem uma conta?',
      'footer.signup': 'Criar conta agora',
      'footer.hasaccount': 'Já tem uma conta?',
      'footer.signin': 'Iniciar sessão',
      // profile
      'profile.title': 'Perfil',
      'profile.memberSince': 'Membro desde',
      'profile.enrolled': 'Inscrito',
      'profile.completed': 'Concluído',
      'profile.saved': 'Guardado',
      'profile.signout': 'Terminar sessão',
      'profile.language': 'Idioma',
      'profile.languageHint': 'Escolha o idioma do site',
      // new Kutiva footer (footer.png)
      'footer.podcasts': 'Ouça Nossos Podcasts',
      'footer.nanodegrees': 'Nanodegrees',
      'footer.programas': 'Programas',
      'footer.sobre': 'Sobre',
      'footer.comunidade': 'Comunidade',
      'footer.contacto': 'Contacto',
      'footer.direitos': 'Direitos Autorais',
      'footer.privacidade': 'Politica de privacidade',
      'footer.termos': 'Termos e condições',
      'footer.copy': 'Kutiva 2022. Todos os direitos reservados',
      'footer.copy_suffix': 'Todos os direitos reservados'
    },
    en: {
      'landing.nav.courses': 'COURSES',
      'landing.nav.programs': 'PROGRAMS',
      'landing.nav.community': 'COMMUNITY',
      'landing.nav.mycourses': 'MY COURSES',
      'landing.nav.openpanel': 'Open dashboard',
      'landing.nav.login': 'SIGN IN',
      'landing.nav.signup': 'Sign up',
      'landing.hero.title': 'SECURE YOUR FUTURE BY LEARNING NEW SKILLS ONLINE.',
      'landing.hero.subtitle': 'Join thousands of students and learn with hands-on courses at your own pace, with professional certification.',
      'landing.hero.cta': 'Get started now',
      'landing.band.title': 'LEARN THE TECHNOLOGIES USED BY THE WORLD’S BEST SOFTWARE COMPANIES',
      'landing.band.desc': 'Master the tools that top companies use every day — from backend to frontend, with real projects and modern tech.',
      'landing.courses.title': 'Choose your course...',
      'landing.courses.explore': 'Explore All Courses ⟶',
      'landing.careers.title': 'WE BUILD CAREERS THROUGH EDUCATION',
      'landing.careers.subtitle': 'Subscribe and get updates',
      'landing.careers.placeholder': 'Your email',
      'landing.careers.btn': 'SUBSCRIBE',
      'landing.footer.nav': 'Navigation',
      'landing.footer.courses': 'Courses',
      'landing.footer.about': 'About',
      'landing.footer.copy': '© 2026 Academy. All rights reserved.',
      'dash.search.placeholder': 'Search classes, digital products, teachers',
      'dash.mycourses': 'My Classes',
      'dash.allclasses': 'All Classes',
      'dash.discover': 'Discover',
      'dash.results': 'Results',
      'dash.noclasses': 'No classes found',
      'dash.noclasses.sub': 'Try a different search or category.',
      'dash.explore': 'Explore',
      'dash.learn': 'Learn',
      'dash.saved': 'Saved',
      'dash.profile': 'Profile',
      'dash.signin': 'Sign in',
      'dash.signup': 'Sign up',
      'dash.notification.title': 'Notifications',
      'dash.notification.empty': 'No notifications yet.',
      'dash.signout': 'Sign out',
      'login.title': 'Sign In',
      'login.subtitle': 'Welcome back. Sign in to continue',
      'signup.title': 'Sign Up',
      'signup.subtitle': 'Create your account to continue',
      'oauth.github': 'Continue with GitHub',
      'oauth.google': 'Continue with Google',
      'oauth.agentmail': 'Continue with AgentMail',
      'divider.or': 'or',
      'field.email': 'Email',
      'field.password': 'Password',
      'field.firstname': 'First name',
      'field.lastname': 'Last name',
      'field.confirm': 'Confirm password',
      'forgot': 'Forgot password?',
      'hint.password': 'Use 8–32 characters with uppercase, lowercase, number and special character.',
      'placeholder.email': 'example@email.com',
      'placeholder.password.login': '•••••',
      'placeholder.password.create': 'Create a strong password',
      'placeholder.password.confirm': 'Confirm your password',
      'btn.signin': 'Sign In',
      'btn.signup': 'Create Account',
      'footer.noaccount': "Don't have an account?",
      'footer.signup': 'Sign Up Now',
      'footer.hasaccount': 'Already have an account?',
      'footer.signin': 'Sign In',
      'profile.title': 'Profile',
      'profile.memberSince': 'Member since',
      'profile.enrolled': 'Enrolled',
      'profile.completed': 'Completed',
      'profile.saved': 'Saved',
      'profile.signout': 'Sign out',
      'profile.language': 'Language',
      'profile.languageHint': 'Choose site language',
      'footer.podcasts': 'Listen to Our Podcasts',
      'footer.nanodegrees': 'Nanodegrees',
      'footer.programas': 'Programs',
      'footer.sobre': 'About',
      'footer.comunidade': 'Community',
      'footer.contacto': 'Contact',
      'footer.direitos': 'Copyright',
      'footer.privacidade': 'Privacy Policy',
      'footer.termos': 'Terms and Conditions',
      'footer.copy': 'Kutiva 2022. All rights reserved',
      'footer.copy_suffix': 'All rights reserved'
    }
  };
  function applyLang(lang){
    if(!dict[lang]) lang='pt';
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var k=el.getAttribute('data-i18n');
      if(dict[lang][k]!==undefined) el.textContent=dict[lang][k];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el){
      var k=el.getAttribute('data-i18n-placeholder');
      if(dict[lang][k]!==undefined) el.setAttribute('placeholder', dict[lang][k]);
    });
    document.querySelectorAll('.lang-switch button').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-lang')===lang);
    });
    try{ localStorage.setItem('academy_lang', lang); }catch(e){}
    try{ document.cookie='academy_lang='+lang+';path=/;max-age=31536000'; }catch(e){}
    // update server via i18n endpoint (optional, no reload)
    try{
      var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
      if(csrftoken){
        fetch('/i18n/setlang/', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':csrftoken}, body:'language='+lang});
      }
    }catch(e){}
  }
  var stored=null; try{ stored=localStorage.getItem('academy_lang'); }catch(e){}
  var browser=(navigator.language||navigator.userLanguage||'').toLowerCase();
  var browserLang=browser.startsWith('en')?'en':'pt';
  // also respect cookie academy_lang if no localStorage
  try{
    var m=document.cookie.match(/(?:^|; )academy_lang=(pt|en)/);
    if(!stored && m) stored=m[1];
  }catch(e){}
  var initial=stored||browserLang;
  try{ if(!stored) localStorage.setItem('academy_lang', browserLang); }catch(e){}
  try{ document.cookie='academy_lang='+initial+';path=/;max-age=31536000'; }catch(e){}
  window.__academySetLang=applyLang;
  window.__academyDict=dict;
  function bind(){
    document.querySelectorAll('.lang-switch button').forEach(function(b){
      b.addEventListener('click', function(){ applyLang(b.getAttribute('data-lang')); });
    });
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', function(){ applyLang(initial); bind(); });
  } else { applyLang(initial); bind(); }
  // expose for SPA-like re-apply after dynamic content
  document.addEventListener('academy:lang', function(e){ applyLang(e.detail||initial); });
})();
