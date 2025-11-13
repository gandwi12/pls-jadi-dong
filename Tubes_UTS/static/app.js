// Minimal frontend logic for cart and simple interactions
const Cart = {
  items: [],
  deliveryFee: 10000,
  discount(){ const s = this.totalPrice(); return s >= 50000 ? Math.floor(s * 0.1) : 0 },
  add(item) {
    const found = this.items.find(i => i.id == item.id)
    if (found) found.qty += 1
    else this.items.push({...item, qty:1})
    this.save()
    this.renderMini()
    this.renderCartList()
    this.renderPaymentSummary()
    
    // Show notification
    this.showNotification(`${item.name} ditambahkan ke keranjang!`, 'success')
  },
  showNotification(message, type = 'info') {
    // Create notification element
    const notif = document.createElement('div')
    notif.className = `notification notification-${type}`
    notif.innerHTML = `
      <div class="notification-content">
        <i class="fas fa-check-circle"></i> ${message}
      </div>
    `
    document.body.appendChild(notif)
    
    // Animate in
    setTimeout(() => notif.classList.add('show'), 10)
    
    // Remove after 3 seconds
    setTimeout(() => {
      notif.classList.remove('show')
      setTimeout(() => notif.remove(), 300)
    }, 3000)
  },
  remove(id) {
    this.items = this.items.filter(i => i.id != id)
    this.save(); this.renderMini(); this.renderCartList(); this.renderPaymentSummary()
  },
  changeQty(id, delta) {
    const it = this.items.find(i=>i.id==id)
    if(!it) return
    it.qty = Math.max(1, it.qty + delta)
    this.save(); this.renderMini(); this.renderCartList(); this.renderPaymentSummary()
  },
  clear() { this.items = []; this.save(); this.renderMini(); this.renderCartList(); this.renderPaymentSummary() },
  save() { localStorage.setItem('fd_cart', JSON.stringify(this.items)) },
  load() { this.items = JSON.parse(localStorage.getItem('fd_cart')||'[]') },
  totalCount(){ return this.items.reduce((s,i)=>s+i.qty,0) },
  totalPrice(){ return this.items.reduce((s,i)=>s + i.qty * (parseFloat(i.price)||0),0) },
  renderMini(){
    const el = document.getElementById('cart-count')
    if(el) el.textContent = this.totalCount()
  },
  renderCartList(){
    const el = document.getElementById('cart-list')
    if(!el) return
    if(this.items.length===0){ el.innerHTML = '<p class="muted">Keranjang kosong.</p>'; return }
    const rows = this.items.map(i=>`
      <div class="cart-row">
        <div class="cart-name">${i.name}</div>
        <div class="cart-qty">
          <button data-id="${i.id}" class="qty-btn qty-dec">-</button>
          <span>${i.qty}</span>
          <button data-id="${i.id}" class="qty-btn qty-inc">+</button>
        </div>
        <div class="cart-sub">Rp ${ (i.qty * (parseFloat(i.price)||0)).toFixed(0) }</div>
        <button data-id="${i.id}" class="btn small remove">Hapus</button>
      </div>
    `).join('')
    el.innerHTML = rows
    // attach handlers
    el.querySelectorAll('.qty-dec').forEach(b=>b.addEventListener('click',e=>{Cart.changeQty(e.target.dataset.id,-1)}))
    el.querySelectorAll('.qty-inc').forEach(b=>b.addEventListener('click',e=>{Cart.changeQty(e.target.dataset.id,1)}))
    el.querySelectorAll('.remove').forEach(b=>b.addEventListener('click',e=>{Cart.remove(e.target.dataset.id)}))
    this.renderPaymentSummary()
  },
  renderPaymentSummary(){
    const subtotal = this.totalPrice()
    const subtotalEl = document.getElementById('payment-subtotal')
    if(subtotalEl) subtotalEl.textContent = 'Rp ' + Number(subtotal).toLocaleString('id-ID')
    const deliveryFee = this.deliveryFee
    const discount = this.discount()
    const discountEl = document.getElementById('payment-discount')
    if(discountEl) discountEl.textContent = '- Rp ' + Number(discount).toLocaleString('id-ID')
    const totalEl = document.getElementById('payment-total')
    if(totalEl) totalEl.textContent = 'Rp ' + Number(subtotal + deliveryFee - discount).toLocaleString('id-ID')
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  Cart.load(); Cart.renderMini(); Cart.renderCartList(); Cart.renderPaymentSummary()

  document.querySelectorAll('.add-to-cart').forEach(btn=>{
    btn.addEventListener('click', e=>{
      const id = btn.dataset.id
      const name = btn.dataset.name
      const price = btn.dataset.price
      Cart.add({id,name,price})
    })
  })

  const orderForm = document.getElementById('order-form')
  if(orderForm){
    orderForm.addEventListener('submit', e=>{
      e.preventDefault()
      if(Cart.items.length===0){ Cart.showNotification('Keranjang kosong!', 'info'); return }
      // Simple submit: send POST to /order (backend should accept JSON)
      fetch('/order', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({cart:Cart.items, name: orderForm.name.value, address: orderForm.address.value, note: orderForm.note.value})
      }).then(r=>{
        if(r.ok){
          r.json().then(function(d){ if(d && d.id) localStorage.setItem('fd_order_id', JSON.stringify(d.id)) }).catch(function(){})
          // don't clear cart here — proceed to payment page which reads cart from localStorage
          Cart.showNotification('Pesanan dibuat', 'success');
          const pending = { items: Cart.items, subtotal: Cart.totalPrice(), name: orderForm.name.value, address: orderForm.address.value, note: orderForm.note.value, ts: Date.now() }
          localStorage.setItem('fd_pending_order', JSON.stringify(pending))
          setTimeout(()=>{ window.location='/payment' }, 1000)
        }
        else Cart.showNotification('Gagal membuat pesanan', 'info')
      }).catch(()=>Cart.showNotification('Gagal menghubungi server', 'info'))
    })
  }

  const paymentForm = document.getElementById('payment-form')
  if(paymentForm){
    paymentForm.addEventListener('submit', e=>{
      e.preventDefault()
      const method = (paymentForm.method && paymentForm.method.value) || 'cod'
      const subtotal = Cart.totalPrice()
      const deliveryFee = Cart.deliveryFee
      const discount = Cart.discount()
      const total = subtotal + deliveryFee - discount
      const pending = JSON.parse(localStorage.getItem('fd_pending_order')||'{}')
      const orderRecord = {
        items: Cart.items,
        subtotal,
        deliveryFee,
        discount,
        total,
        method,
        name: pending.name || '',
        address: pending.address || '',
        note: pending.note || '',
        ts: Date.now()
      }
      const payloadItems = Cart.items.map(i=>({id:i.id, name:i.name, qty:i.qty, price: i.price}))
      const ensureOrder = (function(){
        const existingId = JSON.parse(localStorage.getItem('fd_order_id')||'null')
        if(existingId) return Promise.resolve({id: existingId})
        return fetch('/order', {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({items: payloadItems})
        }).then(r=> r.ok ? r.json() : null).catch(()=>null)
      })()
      ensureOrder.then(data=>{
        const orderId = data && data.id
        if(orderId){
          orderRecord.order_id = orderId
          localStorage.setItem('fd_order_id', JSON.stringify(orderId))
          fetch('/payment', {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({order_id: orderId, amount: total, method, status: 'success'})
          }).catch(()=>{})
        }
        const history = JSON.parse(localStorage.getItem('fd_order_history')||'[]')
        history.unshift(orderRecord)
        localStorage.setItem('fd_order_history', JSON.stringify(history))
        const txs = JSON.parse(localStorage.getItem('fd_transactions')||'[]')
        txs.unshift({ amount: total, type: 'debit', description: 'Pembayaran pesanan - ' + method, ts: orderRecord.ts })
        localStorage.setItem('fd_transactions', JSON.stringify(txs))
        localStorage.removeItem('fd_pending_order')
        localStorage.removeItem('fd_order_id')
        Cart.clear(); Cart.showNotification('Pembayaran dicatat. Terima kasih!', 'success'); setTimeout(()=>{ window.location='/' }, 1200)
      })
    })
  }
})
