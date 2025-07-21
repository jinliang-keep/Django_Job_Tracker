document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-job-btn').forEach(function(btn) {
        btn.addEventListener('click', function(event) {
            event.preventDefault();
            const jobId = this.getAttribute('data-id');

            //向后端请求职位信息
            fetch(`/job_detail/${jobId}/`)
                .then(response => {
                    if(!response.ok){
                        throw new Error("请求失败");
                    }
                    return response.json();
                })
                .then(data => {
                    // 填充表单字段 
                    document.getElementById('job_id').value = data.job_id || '';
                    document.getElementById('company').value = data.company || '';
                    document.getElementById('title').value = data.title || '';
                    document.getElementById('salary').value = data.salary || '';
                    document.getElementById('location').value = data.location || '';
                    document.getElementById('status').value = data.status || '';
                    document.getElementById('note').value = data.note || '';
                    document.getElementById('date_applied').value = data.date_applied || '';
                    document.getElementById('link').value = data.link || '';

                    // 修改模态框标题
                    document.getElementById('addModalLabel').textContent = '编辑职位';
            
                    // 弹出模态框
                    const myModal = new bootstrap.Modal(document.getElementById('addJobModal'));
                    myModal.show();
                })

                .catch(error => {
                    console.error('获取职位数据失败：', error);
                    alert('加载职位数据失败，请稍后重试');
                })
        })
    })
})