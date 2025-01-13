# TODO: Make it easy to install dependencies
conda activate llm_agent
absolute_userdata_path=$(realpath "test_data.json")
absolute_jobdescription_path=$(realpath "job_description.txt")

echo $absolute_jobdescription_path
echo $absolute_userdata_path

python src/llm_resume_critique.py $absolute_userdata_path $absolute_jobdescription_path
python src/resume_builder.py
echo "Done!"