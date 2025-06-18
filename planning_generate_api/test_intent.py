"""
意图识别功能测试脚本
"""

import asyncio
from intent_detection import detect_bioinformatics_intent, is_bioinformatics_related

async def test_intent_detection():
    """测试意图识别功能"""
    
    # 测试用例
    test_cases = [
        # 生信分析相关的查询
        ("帮我使用时空组学的数据，进行标准分析和下游高级分析", 1),
        ("请帮我分析基因表达数据", 1),
        ("进行蛋白质组学分析", 1),
        ("帮我做代谢组学数据处理", 1),
        ("单细胞测序数据分析", 1),
        ("基因差异表达分析", 1),
        ("生物标志物发现", 1),
        ("通路富集分析", 1),
        ("聚类分析", 1),
        ("序列比对分析", 1),
        
        # 非生信分析相关的查询
        ("今天天气怎么样？", 0),
        ("我想看电影", 0),
        ("帮我写一篇文章", 0),
        ("计算器怎么用", 0),
        ("推荐一些音乐", 0),
        ("如何做菜", 0),
        ("旅游攻略", 0),
        ("数学题求解", 0),
        ("编程学习", 0),
        ("购物推荐", 0)
    ]
    
    print("=== 生物信息学意图识别测试 ===\n")
    
    correct_count = 0
    total_count = len(test_cases)
    
    for query, expected in test_cases:
        try:
            result = await detect_bioinformatics_intent(query)
            is_correct = result == expected
            if is_correct:
                correct_count += 1
                
            status = "✓" if is_correct else "✗"
            print(f"{status} 查询: {query}")
            print(f"   预期: {expected}, 实际: {result}")
            print(f"   结果: {'生信分析相关' if result == 1 else '非生信分析相关'}")
            print("-" * 60)
            
        except Exception as e:
            print(f"✗ 查询: {query}")
            print(f"   错误: {str(e)}")
            print("-" * 60)
    
    accuracy = (correct_count / total_count) * 100
    print(f"\n=== 测试结果 ===")
    print(f"正确识别: {correct_count}/{total_count}")
    print(f"准确率: {accuracy:.1f}%")

if __name__ == "__main__":
    asyncio.run(test_intent_detection()) 