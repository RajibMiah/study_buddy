<template>
  <!-- Modal HTML -->
  <div id="myModal" class="modal fade">
    <div class="modal-dialog modal-confirm">
      <div class="modal-content">
        <div class="modal-header">
          <div class="icon-box">
            <i class="material-icons">&#xE5CD;</i>
          </div>
          <h4 class="modal-title">Are you sure?</h4>
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-hidden="true"
          >
            &times;
          </button>
        </div>
        <div class="modal-body">
          <p>
            Do you really want to delete these records? This process cannot be
            undone.
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-info" data-dismiss="modal">
            Cancel
          </button>
          <button type="button" class="btn btn-danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
#myModal {
  z-index: 99999999999999999;
}
.modal-confirm {
  color: #636363 !important;
  width: 400px !important;
}
.modal-confirm .modal-content {
  padding: 20px !important;
  border-radius: 5px !important;
  border: none !important;
  text-align: center !important;
  font-size: 14px !important;
}
.modal-confirm .modal-header {
  border-bottom: none;
  position: relative !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.modal-confirm h4 {
  text-align: center;
  font-size: 26px !important;
  margin: 30px 0 -10px !important;
}
.modal-confirm .close {
  position: absolute !important;
  top: -5px !important;
  right: -2px !important;
}
.modal-confirm .modal-body {
  color: #999;
}
.modal-confirm .modal-footer {
  border: none;
  margin: 0 auto;
  text-align: center !important;
  border-radius: 5px !important;
  font-size: 13px !important;
  padding: 10px 15px 25px !important;
}
.modal-confirm .modal-footer a {
  color: #999;
}
.modal-confirm .icon-box {
  width: 80px !important;
  height: 80px !important;
  margin: 0 auto !important;
  border-radius: 50% !important;
  z-index: 99 !important;
  text-align: center !important;
  border: 3px solid #f15e5e !important;
}
.modal-confirm .icon-box i {
  color: #f15e5e !important;
  font-size: 46px !important;
  display: inline-block !important;
  margin-top: 13px !important;
}
.modal-confirm .btn {
  display: flex !important;
  justify-content: center;
  text-align: center;
  font-size: 13px;
  color: #fff !important;
  border-radius: 4px !important;
  background: #60c7c1 !important;
  text-decoration: none !important;
  transition: all 0.4s !important;
  line-height: normal !important;
  min-width: 120px !important;
  border: none !important;
  min-height: 40px !important;
  border-radius: 3px !important;
  margin: 0 5px !important;
  outline: none !important;
}
.modal-confirm .btn-info {
  background: #c1c1c1 !important;
}
.modal-confirm .btn-info:hover,
.modal-confirm .btn-info:focus {
  background: #a8a8a8 !important;
}
.modal-confirm .btn-danger {
  background: #f15e5e !important;
}
.modal-confirm .btn-danger:hover,
.modal-confirm .btn-danger:focus {
  background: #ee3535 !important;
}
.trigger-btn {
  display: inline-block !important;
  margin: 100px auto !important;
}
</style>
