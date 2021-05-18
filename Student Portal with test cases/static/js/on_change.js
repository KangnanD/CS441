$(document).on('change','#assignee',function(){
Swal.fire({
  title: 'You want to change the assignee ?',
  text: "You won't be able to revert this!",
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, Change Please!'
}).then((result) => {
   if (result.isConfirmed) {
   let assignee = $('#assignee').val();
   let jira_id = $('#jira_id').val();
      $.ajax({
      type: "GET",
      url: "/api/update/jira/assignee",
      data: {"assignee":assignee,"jira_id":jira_id},
      cache: false,
      success: function(data){
        Swal.fire(
          'Changed!',
          'the assignee has been changed.',
          'success'
        )
      },
      error:function(data){
        Swal.fire(
          'Error!',
          'please try after some time.',
          'error'
        )
      }
    });
}
})
});
$(document).on('change','#status',function(){
Swal.fire({
  title: 'You want to change the status ?',
  text: "You won't be able to revert this!",
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, Change it!'
}).then((result) => {
  if (result.isConfirmed) {
   let status = $('#status').val();
   let jira_id = $('#jira_id').val();
      $.ajax({
      type: "POST",
      url: "/api/update/jira/status",
      data: {"status":status,"jira_id":jira_id},
      cache: false,
      success: function(data){
        Swal.fire(
          'Changed!',
          'the status has been changed.',
          'success'
        ).then(function(){
            window.location.reload(true);
        });
      },
      error:function(data){
        Swal.fire(
          'Error!',
          'please try after some time.',
          'error'
        )
      }
    });
  }
})
});