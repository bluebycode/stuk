class CreateMachines < ActiveRecord::Migration[5.2]
  def change
    create_table :machines do |t|
      t.string :name
      t.string :ip
      t.string :sequence

      t.timestamps
    end
  end
end
