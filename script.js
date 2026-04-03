function getSourceIcon(source) {
  switch(source) {
    case "WHO": return "🌍";
    case "CDC": return "🛡️";
    case "UNICEF": return "👶";
    case "Fallback": return "💡";
    default: return "ℹ️";
  }
}

async function loadLatest() {
  try {
    const res = await fetch('data/tips/latest.json?nocache=' + Date.now());
    const tips = await res.json();
    const container = document.getElementById('tips-container');
    container.innerHTML = '';
    tips.forEach(tip => {
      container.innerHTML += `
        <div class="tip-card">
          <h5 class="fw-bold mb-2">${tip.content}</h5>
          <span class="source-label">${getSourceIcon(tip.source)} القسم: ${tip.category} | المصدر: ${tip.source}</span>
        </div>
      `;
    });
  } catch (err) {
    console.error("خطأ في تحميل النصائح:", err);
    document.getElementById('tips-container').innerHTML = "<p>⚠️ تعذر تحميل النصائح.</p>";
  }
}

async function loadArchive() {
  try {
    const today = new Date().toISOString().split('T')[0];
    const res = await fetch(`data/tips/archive-${today}.json?nocache=${Date.now()}`);
    const tips = await res.json();
    const container = document.getElementById('tips-container');
    container.innerHTML = '';
    tips.forEach(tip => {
      container.innerHTML += `
        <div class="tip-card">
          <h5 class="fw-bold mb-2">${tip.content}</h5>
          <span class="source-label">${getSourceIcon(tip.source)} القسم: ${tip.category} | المصدر: ${tip.source}</span>
        </div>
      `;
    });
  } catch (err) {
    console.error("خطأ في تحميل الأرشيف:", err);
    document.getElementById('tips-container').innerHTML = "<p>⚠️ تعذر تحميل الأرشيف.</p>";
  }
}

// تشغيل عند فتح الصفحة
loadLatest();
