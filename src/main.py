# 导入第三方库
import os

# 导入项目函数
import mydata
import bayesian_analysis
import output

def main():

    # 使用参数解析模块获取命令行参数
    #args = arguments.parse_arguments()

    #k = args.k
    #mantissa = args.mantissa
    #exponent = args.exponent
    #job_name = args.job_name


    # these parameters are used for test
    k = 3
    mantissa = 2
    exponent = 2
    job_name = "src"


    total = int(mantissa * 10**exponent)
    draws = total //2
    tune = total // 2


    # 构建完整的输出目录路径
    output_directory = os.path.join("../data", job_name)

    # 确保输出目录存在，如果不存在则创建它
    os.makedirs(output_directory, exist_ok=True)

    # 重定向输出结果到文件
    output.redirect_output(output_directory)

    # 调用数据导入和预处理模块
    ages, zircons_data = mydata.process_data()

    # 调用贝叶斯分析模块，传递处理完的数据
    trace = bayesian_analysis.perform_bayesian_analysis(k, tune, draws, ages, zircons_data, output_directory)

    # 设置要输出的内容
    # 输出trace（后验分布的结果）
    output.save_trace(trace, output_directory)
    # 输出histogram
    output.save_histogram(ages, zircons_data, output_directory)
    # 输出scatter
    output.save_scatter_plot(ages, zircons_data,output_directory)

    # 恢复标准输出
    output.restore_output()

if __name__ == "__main__":
    main()