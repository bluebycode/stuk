class MachinesController < ApplicationController

  def create
    @machine = Machine.new(machine_params)

    respond_to do |format|
      if @machine.save
        format.html { redirect_to root_path, notice: 'Machine was successfully created.' }
      end
    end
  end

  # Use callbacks to share common setup or constraints between actions.
  def set_machine
    @machine = Machine.find(params[:id])
  end

  # Never trust parameters from the scary internet, only allow the white list through.
  def machine_params
    params.require(:machine).permit(:name, :ip, :sequence, :image_src)
  end
end
