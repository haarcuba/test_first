tests = FileList[ 'startertests/**/startertest*.py' ]
tests.each do |test|
    task test do
        sh "python #{test}"
    end
end

task :starter_tests => tests.to_a

task :examples do
    sh "python3 -m unittest examples/tests/test_*.py"
end
