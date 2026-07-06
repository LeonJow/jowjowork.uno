---
title: 商业合作
date: 2026-07-06T16:00:00+08:00
draft: false
description: 提交商业合作项目信息，我将评估可行性后与你联系
layout: cooperation
---
<div class="cooperation-intro">
  <p>如果你有商业合作项目、外包需求或创意想法，欢迎填写以下表单。</p>
  <p>我会在 <strong>3 个工作日内</strong>评估可行性并回复你。</p>
</div>

<form id="cooperation-form" action="https://formsubmit.io/send/jowjowork@163.com" method="POST" class="cooperation-form">
  <input type="hidden" name="_subject" value="新合作项目提交 - JowJow Work">
  <input type="text" name="_honey" style="display:none">
  <input type="hidden" name="_template" value="box">
  <input type="hidden" name="_captcha" value="true">

  <div class="form-group">
    <label for="project-name">项目名称 *</label>
    <input type="text" id="project-name" name="项目名称" required placeholder="例如：企业官网开发">
  </div>

  <div class="form-row">
    <div class="form-group">
      <label for="contact-name">联系人 *</label>
      <input type="text" id="contact-name" name="联系人" required placeholder="你的姓名">
    </div>
    <div class="form-group">
      <label for="contact-email">邮箱 *</label>
      <input type="email" id="contact-email" name="联系邮箱" required placeholder="your@email.com">
    </div>
  </div>

  <div class="form-row">
    <div class="form-group">
      <label for="contact-phone">手机号</label>
      <input type="tel" id="contact-phone" name="联系电话" placeholder="选填">
    </div>
    <div class="form-group">
      <label for="company">公司/组织</label>
      <input type="text" id="company" name="公司或组织" placeholder="选填">
    </div>
  </div>

  <div class="form-group">
    <label for="project-type">项目类型 *</label>
    <select id="project-type" name="项目类型" required>
      <option value="">请选择...</option>
      <option value="网站开发">网站开发</option>
      <option value="小程序开发">小程序开发</option>
      <option value="自动化工具">自动化工具</option>
      <option value="内容创作">内容创作</option>
      <option value="技术咨询">技术咨询</option>
      <option value="合作创业">合作创业</option>
      <option value="其他">其他</option>
    </select>
  </div>

  <div class="form-group">
    <label for="description">项目描述 *</label>
    <textarea id="description" name="项目描述" rows="6" required placeholder="请详细描述项目内容、需求背景、目标用户等..."></textarea>
  </div>

  <div class="form-row">
    <div class="form-group">
      <label for="budget">预算范围</label>
      <select id="budget" name="预算范围">
        <option value="未确定">未确定</option>
        <option value="1000元以下">1000元以下</option>
        <option value="1000-5000元">1,000 - 5,000 元</option>
        <option value="5000-10000元">5,000 - 10,000 元</option>
        <option value="10000-50000元">10,000 - 50,000 元</option>
        <option value="50000元以上">50,000 元以上</option>
      </select>
    </div>
    <div class="form-group">
      <label for="timeline">期望时间</label>
      <select id="timeline" name="期望时间">
        <option value="未确定">未确定</option>
        <option value="1周内">1 周内</option>
        <option value="2周内">1 - 2 周</option>
        <option value="1个月内">1 个月内</option>
        <option value="1-3个月">1 - 3 个月</option>
        <option value="3个月以上">3 个月以上</option>
      </select>
    </div>
  </div>

  <div class="form-group">
    <label for="reference">参考案例 / 附加说明</label>
    <textarea id="reference" name="参考案例或附加说明" rows="3" placeholder="如有参考网站、设计稿或更多补充信息，请填写链接或说明（选填）"></textarea>
  </div>

  <button type="submit" class="form-submit">提交合作意向</button>

</form>

<div id="form-success" style="display:none;">
  <div class="success-message">
    <span class="success-icon">✅</span>
    <h2>提交成功！</h2>
    <p>感谢你的合作意向，我会在 <strong>3 个工作日内</strong>评估并回复到你的邮箱。</p>
    <p><a href="/" style="color: var(--link-color, #7c3aed);">← 返回首页</a></p>
  </div>
</div>

<style>
.cooperation-intro {
  background: var(--entry, #1a1a2e);
  border: 1px solid var(--border, #2d2d4f);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 28px;
  font-size: 0.95em;
  line-height: 1.7;
}
.cooperation-intro p { margin: 0 0 6px; }
.cooperation-intro p:last-child { margin-bottom: 0; }

.cooperation-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}
@media (max-width: 600px) {
  .form-row { grid-template-columns: 1fr; }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.9em;
  font-weight: 600;
  color: var(--primary, #7c3aed);
}

.form-group input,
.form-group select,
.form-group textarea {
  background: var(--entry, #1a1a2e);
  border: 1px solid var(--border, #2d2d4f);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.95em;
  color: var(--primary, #e2e2f0);
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--tertiary, #555);
}

.form-group select {
  cursor: pointer;
}

.form-group select option {
  background: var(--theme, #0a0a1a);
  color: var(--primary, #e2e2f0);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-submit {
  background: #7c3aed;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 14px 32px;
  font-size: 1.05em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  align-self: flex-start;
  letter-spacing: 0.5px;
}

.form-submit:hover {
  background: #6d28d9;
  transform: translateY(-1px);
}

.form-submit:active {
  transform: translateY(0);
}

.success-message {
  text-align: center;
  padding: 48px 24px;
  background: var(--entry, #1a1a2e);
  border: 1px solid var(--border, #2d2d4f);
  border-radius: 12px;
}

.success-icon {
  font-size: 3em;
  display: block;
  margin-bottom: 16px;
}

.success-message h2 {
  margin: 0 0 12px;
  font-size: 1.5em;
}

.success-message p {
  color: var(--secondary, #999);
  line-height: 1.6;
}
</style>

<script>
document.getElementById('cooperation-form').addEventListener('submit', function(e) {
  // Show loading state
  const btn = this.querySelector('.form-submit');
  btn.textContent = '提交中...';
  btn.disabled = true;
});
</script>
